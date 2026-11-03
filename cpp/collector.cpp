
#include <condition_variable>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <queue>
#include <random>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

struct Reading {
    int device;
    int seq;
    double temp_c;
    double power_w;
    bool unhealthy;
};

class BoundedQueue {
    std::queue<Reading> q_;
    const std::size_t capacity_;
    std::mutex mu_;
    std::condition_variable not_empty_;
    std::condition_variable not_full_;
    bool closed_ = false;

public:
    explicit BoundedQueue(std::size_t capacity) : capacity_(capacity) {
        if (capacity == 0)
            throw std::invalid_argument("Queue capacity must be positive");
    }

    bool push(Reading reading) {
        std::unique_lock<std::mutex> lock(mu_);

        not_full_.wait(lock, [&] {
            return closed_ || q_.size() < capacity_;
        });

        if (closed_) return false;

        q_.push(reading);
        lock.unlock();
        not_empty_.notify_one();
        return true;
    }

    bool pop(Reading& reading) {
        std::unique_lock<std::mutex> lock(mu_);

        not_empty_.wait(lock, [&] {
            return closed_ || !q_.empty();
        });

        if (q_.empty()) return false;

        reading = q_.front();
        q_.pop();

        lock.unlock();
        not_full_.notify_one();
        return true;
    }

    void close() {
        {
            std::lock_guard<std::mutex> lock(mu_);
            closed_ = true;
        }

        not_empty_.notify_all();
        not_full_.notify_all();
    }
};

int main(int argc, char** argv) {
    std::string output = argc > 1 ? argv[1] : "telemetry.jsonl";
    int devices = 4;
    int samples = 50;

    try {
        if (argc > 2) devices = std::stoi(argv[2]);
        if (argc > 3) samples = std::stoi(argv[3]);
    } catch (const std::exception&) {
        std::cerr << "Invalid devices/samples\n";
        return 2;
    }

    if (devices < 1 || devices > 100 ||
        samples < 1 || samples > 100000) {
        std::cerr << "Invalid devices/samples\n";
        return 2;
    }

    std::ofstream f(output);
    if (!f) {
        std::cerr << "Unable to open " << output << "\n";
        return 1;
    }

    BoundedQueue readings(64);
    int total = 0;
    int unhealthy = 0;

    // Consumer processes readings while producers are running.
    std::thread consumer([&] {
        Reading r;

        while (readings.pop(r)) {
            f << std::fixed << std::setprecision(2)
              << "{\"device_id\":\"node-" << r.device
              << "\",\"sequence\":" << r.seq
              << ",\"temp_c\":" << r.temp_c
              << ",\"power_w\":" << r.power_w
              << ",\"unhealthy\":"
              << (r.unhealthy ? "true" : "false")
              << "}\n";

            ++total;
            unhealthy += r.unhealthy;
        }
    });

    // Each simulated device runs in its own producer thread.
    std::vector<std::thread> workers;

    for (int d = 0; d < devices; ++d) {
        workers.emplace_back([&, d] {
            std::mt19937 rng(42 + d);
            std::normal_distribution<double> jitter(0, 2.5);

            for (int s = 0; s < samples; ++s) {
                double temp =
                    62.0 + jitter(rng) +
                    ((s % 25 == 24) ? 26.0 : 0.0);

                double watts = 185.0 + jitter(rng) * 4.0;

                if (!readings.push({
                        d, s, temp, watts,
                        temp >= 80.0 || watts >= 240.0
                    })) {
                    return;
                }
            }
        });
    }

    for (auto& worker : workers) {
        worker.join();
    }

    // No more readings will arrive. Drain queue and exit.
    readings.close();
    consumer.join();

    f.close();
    if (!f) {
        std::cerr << "Error writing " << output << "\n";
        return 1;
    }

    std::cout << "Generated " << total
              << " readings; unhealthy=" << unhealthy
              << "; file=" << output << "\n";

    return 0;
}

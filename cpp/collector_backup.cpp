#include <atomic>
#include <chrono>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <queue>
#include <random>
#include <sstream>
#include <string>
#include <thread>
#include <vector>

struct Reading { int device; int seq; double temp_c; double power_w; bool unhealthy; };
class Queue {
    std::queue<Reading> q;
    std::mutex mu;
public:
    void push(Reading r) { std::lock_guard<std::mutex> lock(mu); q.push(r); }
    bool pop(Reading& r) { std::lock_guard<std::mutex> lock(mu); if(q.empty()) return false; r=q.front(); q.pop(); return true; }
};
int main(int argc, char** argv) {
    std::string output = argc>1 ? argv[1] : "telemetry.jsonl";
    int devices = argc>2 ? std::stoi(argv[2]) : 4;
    int samples = argc>3 ? std::stoi(argv[3]) : 50;
    if(devices<1 || devices>100 || samples<1 || samples>100000) { std::cerr<<"Invalid devices/samples\n"; return 2; }
    Queue readings;
    std::vector<std::thread> workers;
    for(int d=0; d<devices; ++d) workers.emplace_back([&,d]{
        std::mt19937 rng(42+d); std::normal_distribution<double> jitter(0, 2.5);
        for(int s=0; s<samples; ++s) {
            double temp=62.0+jitter(rng)+((s%25==24)?26.0:0.0);
            double watts=185.0+jitter(rng)*4.0;
            readings.push({d,s,temp,watts,temp>=80.0 || watts>=240.0});
        }
    });
    for(auto& worker:workers) worker.join();
    std::ofstream f(output); if(!f) { std::cerr<<"Unable to open "<<output<<"\n"; return 1; }
    Reading r; int total=0, unhealthy=0;
    while(readings.pop(r)) {
        f<<std::fixed<<std::setprecision(2)<<"{\"device_id\":\"node-"<<r.device
         <<"\",\"sequence\":"<<r.seq<<",\"temp_c\":"<<r.temp_c
         <<",\"power_w\":"<<r.power_w<<",\"unhealthy\":"<<(r.unhealthy?"true":"false")<<"}\n";
        ++total; unhealthy+=r.unhealthy;
    }
    std::cout<<"Generated "<<total<<" readings; unhealthy="<<unhealthy<<"; file="<<output<<"\n";
}

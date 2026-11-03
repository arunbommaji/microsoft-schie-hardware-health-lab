
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <vector>

class UARTFrame {
public:
    static constexpr uint8_t START = 0xAA;

    static std::vector<uint8_t> encode(
        const std::vector<uint8_t>& payload
    ) {
        if (payload.empty() || payload.size() > 255)
            throw std::invalid_argument("Invalid payload size");

        std::vector<uint8_t> frame = {
            START,
            static_cast<uint8_t>(payload.size())
        };

        uint8_t checksum = frame[1];

        for (uint8_t byte : payload) {
            frame.push_back(byte);
            checksum ^= byte;
        }

        frame.push_back(checksum);
        return frame;
    }

    static std::vector<uint8_t> decode(
        const std::vector<uint8_t>& frame
    ) {
        if (frame.size() < 4 || frame[0] != START)
            throw std::runtime_error("Invalid UART frame");

        const auto length = frame[1];

        if (length == 0 || frame.size() != static_cast<std::size_t>(length) + 3U)
            throw std::runtime_error("Invalid UART frame length");

        uint8_t checksum = length;

        for (std::size_t i = 2; i < frame.size() - 1; ++i)
            checksum ^= frame[i];

        if (checksum != frame.back())
            throw std::runtime_error("UART checksum mismatch");

        return {
            frame.begin() + 2,
            frame.end() - 1
        };
    }
};

int main() {
    try {
        auto frame = UARTFrame::encode({0x19, 0x80});
        auto payload = UARTFrame::decode(frame);

        std::cout << "UART frame decoded successfully\n";
        std::cout << "Payload bytes: " << payload.size() << "\n";

        frame.back() ^= 0xFF;

        try {
            UARTFrame::decode(frame);
            return 1;
        } catch (const std::runtime_error&) {
            std::cout << "Corrupted checksum: detected\n";
        }

    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }

    return 0;
}


#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <stdexcept>

class SimulatedSPIDevice {
    std::map<uint8_t, uint8_t> registers_;

public:
    SimulatedSPIDevice() {
        registers_[0x00] = 0xAB;  // Device identity
        registers_[0x01] = 0x01;  // Status
        registers_[0x02] = 0x00;  // Configuration
    }

    uint8_t transfer(uint8_t command, uint8_t value = 0) {
        bool write = (command & 0x80) != 0;
        uint8_t address = command & 0x7F;

        if (registers_.find(address) == registers_.end()) {
            throw std::out_of_range("Invalid SPI register");
        }

        if (write) {
            registers_[address] = value;
            return 0;
        }

        return registers_[address];
    }
};

int main() {
    try {
        SimulatedSPIDevice device;

        std::cout << "Simulated SPI device\n";

        auto identity = device.transfer(0x00);
        std::cout << "Device ID: 0x" << std::hex
                  << std::uppercase << static_cast<int>(identity)
                  << std::dec << "\n";

        device.transfer(0x82, 0x05);

        std::cout << "Configuration: "
                  << static_cast<int>(device.transfer(0x02))
                  << "\n";

        try {
            device.transfer(0x7F);
        } catch (const std::out_of_range&) {
            std::cout << "Invalid SPI command: detected\n";
        }

    } catch (const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }

    return 0;
}

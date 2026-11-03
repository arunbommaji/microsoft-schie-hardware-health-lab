
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>

class SimulatedI2CSensor {
    std::map<uint8_t, uint8_t> registers_;

public:
    SimulatedI2CSensor() {
        setTemperature(25.5);
        registers_[0x02] = 0x01;
    }

    void writeRegister(uint8_t address, uint8_t value) {
        if (address > 0x02)
            throw std::out_of_range("Invalid register address");

        registers_[address] = value;
    }

    uint8_t readRegister(uint8_t address) const {
        auto it = registers_.find(address);

        if (it == registers_.end())
            throw std::out_of_range("Invalid register address");

        return it->second;
    }

    void setTemperature(double temp) {
        int16_t raw = static_cast<int16_t>(temp * 256);

        writeRegister(0x00, static_cast<uint8_t>(raw >> 8));
        writeRegister(0x01, static_cast<uint8_t>(raw & 0xFF));
    }

    double temperatureC() const {
        uint16_t raw =
            (static_cast<uint16_t>(readRegister(0x00)) << 8)
            | readRegister(0x01);

        return static_cast<int16_t>(raw) / 256.0;
    }

    void injectSensorFailure() {
        writeRegister(0x02, 0x00);
    }

    bool healthy() const {
        return readRegister(0x02) == 0x01
            && temperatureC() < 80.0;
    }
};

int main() {
    SimulatedI2CSensor sensor;

    std::cout << std::fixed << std::setprecision(2);

    std::cout << "Normal temperature: "
              << sensor.temperatureC() << " C\n";
    std::cout << "Normal health: "
              << (sensor.healthy() ? "healthy" : "fault") << "\n";

    sensor.setTemperature(90.0);

    std::cout << "Overheating temperature: "
              << sensor.temperatureC() << " C\n";
    std::cout << "Overheating health: "
              << (sensor.healthy() ? "healthy" : "fault") << "\n";

    sensor.setTemperature(25.5);
    sensor.injectSensorFailure();

    std::cout << "Sensor failure health: "
              << (sensor.healthy() ? "healthy" : "fault") << "\n";

    try {
        sensor.readRegister(0xFF);
        return 1;
    } catch (const std::out_of_range&) {
        std::cout << "Invalid register access: detected\n";
    }

    return 0;
}

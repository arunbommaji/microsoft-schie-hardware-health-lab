CXX ?= g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra -Wpedantic -pthread
.PHONY: build test demo clean
build:
	mkdir -p build
	$(CXX) $(CXXFLAGS) cpp/collector.cpp -o build/collector
test:
	python3 -m unittest discover -s tests -v
demo: build
	./build/collector telemetry.jsonl 4 50
clean:
	rm -rf build telemetry.jsonl

package main

import (
	"flag"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/golang/glog"
)

func main() {
	defer glog.Flush()
	flag.Parse()

	// Configuration for devices to monitor - now we'll register each device individually
	configs := []DevicePluginConfig{
		{
			DevicePattern:  "^snd$",
			MaxDevices:     1,
			HostPathPrefix: "/dev/",
		},
		{
			DevicePattern:  "^ttyUSB[0-9]+$",
			MaxDevices:     10,
			HostPathPrefix: "/dev/",
		},
		{
			DevicePattern:  "^ttyACM[0-9]+$",
			MaxDevices:     10,
			HostPathPrefix: "/dev/",
		},
		{
			DevicePattern:  "^video[0-9]+$",
			MaxDevices:     10,
			HostPathPrefix: "/dev/",
		},
	}

	manager := NewDevicePluginManager(configs)
	if err := manager.Start(); err != nil {
		glog.Fatalf("Failed to start device plugin manager: %v", err)
	}
	defer manager.Stop()

	// Watch for signals
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM, syscall.SIGHUP)

	// Main loop
	for {
		select {
		case sig := <-sigChan:
			glog.Infof("Received signal %v, shutting down", sig)
			return
		case <-time.After(5 * time.Second):
			// Periodic health check/log
			glog.V(3).Info("Device plugin running")
		}
	}
}

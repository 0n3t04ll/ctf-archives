#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <string.h>

#define MAX_SENSORS 16
#define CRC_SIZE 4
#define MAX_DATA_SIZE 256

typedef enum {
    CMD_REGISTER_SENSOR = 0x01,
    CMD_DROP_SENSOR = 0x02,
    CMD_READ_TELEMETRY = 0x03,
    CMD_UPDATE_FIRMWARE = 0x04
} CommandType;

typedef struct __attribute__((packed)) {
    uint8_t cmd;
    uint8_t sensor_id;
    uint16_t total_length;
    uint32_t crc32;
} PacketHeader;

typedef struct {
    int in_use;
    uint16_t data_size;
    char *telemetry_data;
} Sensor;

Sensor *active_sensors[MAX_SENSORS];

void handle_register(PacketHeader *header) {
    if (header->sensor_id >= MAX_SENSORS || active_sensors[header->sensor_id] != NULL) return;
    if (header->total_length > MAX_DATA_SIZE || header->total_length <= CRC_SIZE) return;

    Sensor *new_sensor = (Sensor *)malloc(sizeof(Sensor));
    new_sensor->in_use = 1;

    new_sensor->data_size = header->total_length - CRC_SIZE;

    new_sensor->telemetry_data = (char *)malloc(new_sensor->data_size);

    read(0, new_sensor->telemetry_data, new_sensor->data_size);

    active_sensors[header->sensor_id] = new_sensor;
}

void handle_drop(PacketHeader *header) {
    if (header->sensor_id >= MAX_SENSORS || active_sensors[header->sensor_id] == NULL) return;

    free(active_sensors[header->sensor_id]->telemetry_data);
    free(active_sensors[header->sensor_id]);
    active_sensors[header->sensor_id] = NULL;
}

void handle_read(PacketHeader *header) {
    if (header->sensor_id >= MAX_SENSORS || active_sensors[header->sensor_id] == NULL) return;

    write(1, active_sensors[header->sensor_id]->telemetry_data, active_sensors[header->sensor_id]->data_size);
}

void handle_update(PacketHeader *header) {
    if (header->sensor_id >= MAX_SENSORS || active_sensors[header->sensor_id] == NULL) return;
    if (header->total_length > MAX_DATA_SIZE) return;

    Sensor *target = active_sensors[header->sensor_id];

    uint32_t payload_size = header->total_length - CRC_SIZE;

    read(0, target->telemetry_data, payload_size);
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    PacketHeader header;

    printf("Server started\n");

    while (1) {
        if (read(0, &header, sizeof(PacketHeader)) != sizeof(PacketHeader)) break;

        switch (header.cmd) {
            case CMD_REGISTER_SENSOR:
                handle_register(&header);
                break;
            case CMD_DROP_SENSOR:
                handle_drop(&header);
                break;
            case CMD_READ_TELEMETRY:
                handle_read(&header);
                break;
            case CMD_UPDATE_FIRMWARE:
                handle_update(&header);
                break;
            default:
                break;
        }
    }
    return 0;
}
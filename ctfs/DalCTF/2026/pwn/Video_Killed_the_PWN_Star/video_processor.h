#ifndef VIDEO_PROCESSOR_H
#define VIDEO_PROCESSOR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/dict.h>

#define BUFFER_SIZE 256

static const uint8_t TARGET_UUID[16] = {
    0x44, 0x41, 0x4c, 0x43, 0x54, 0x46, 0x32, 0x30,
    0x32, 0x36, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00
};

char *parse_uuid_raw(const char *filename);
void process_video(const char *filename);
void extract_metadata(AVFormatContext *fmt_ctx, const char *filename);

#endif // VIDEO_PROCESSOR_H

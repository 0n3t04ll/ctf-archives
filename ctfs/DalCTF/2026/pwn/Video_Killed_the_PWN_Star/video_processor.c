#include "video_processor.h"

static FILE *g_fp;
static char * volatile g_title;

char *parse_uuid_raw(const char *filename) {
    char uuid_buffer[BUFFER_SIZE];

    FILE *fp = fopen(filename, "rb");
    if (!fp) {
        printf("Could not open file for raw metadata parse\n");
        return NULL;
    }
    g_fp = fp;

    uint32_t box_size;
    uint8_t  box_type[4];
    uint8_t  box_uuid[16];

    while (fread(&box_size, 4, 1, fp) == 1) {
        box_size = __builtin_bswap32(box_size);
        if (fread(box_type, 4, 1, fp) != 1) break;

        if (memcmp(box_type, "uuid", 4) == 0) {
            if (fread(box_uuid, 16, 1, fp) != 1) break;
            if (memcmp(box_uuid, TARGET_UUID, 16) == 0) {
                uint32_t data_len = box_size - 24;
                printf("Processing vendor metadata (%u bytes)...\n", data_len);
                fread(uuid_buffer, 1, data_len, fp); 
                printf("Vendor metadata processed.\n");
                fclose(g_fp);
                g_title = uuid_buffer;
                return g_title;
            }
            fseek(fp, box_size - 24, SEEK_CUR);
        } else {
            fseek(fp, box_size - 8, SEEK_CUR);
        }
    }

    printf("No vendor metadata found\n");
    fclose(fp);
    return NULL;
}

void extract_metadata(AVFormatContext *fmt_ctx, const char *filename) {
    printf("=== Extracting Video Metadata ===\n");

    AVDictionaryEntry *tag = NULL;

    tag = av_dict_get(fmt_ctx->metadata, "title", NULL, 0);
    if (tag) {
        printf("Found title metadata: %s\n", tag->value);
    } else {
        printf("No title metadata found\n");
    }

    tag = av_dict_get(fmt_ctx->metadata, "artist", NULL, 0);
    if (tag) {
        printf("Artist: %s\n", tag->value);
    }

    tag = av_dict_get(fmt_ctx->metadata, "comment", NULL, 0);
    if (tag) {
        printf("Comment: %s\n", tag->value);
    }

    char *raw_meta = parse_uuid_raw(filename);
    if (raw_meta) {
        printf("Raw vendor metadata parsed.\n");
    }

    printf("=== Metadata Processing Complete ===\n");
}

void process_video(const char *filename) {
    AVFormatContext *fmt_ctx = NULL;
    int ret;

    printf("Processing video file: %s\n", filename);

    ret = avformat_open_input(&fmt_ctx, filename, NULL, NULL);
    if (ret < 0) {
        fprintf(stderr, "Error: Could not open video file\n");
        return;
    }

    ret = avformat_find_stream_info(fmt_ctx, NULL);
    if (ret < 0) {
        fprintf(stderr, "Error: Could not find stream information\n");
        avformat_close_input(&fmt_ctx);
        return;
    }

    printf("Format: %s\n", fmt_ctx->iformat->long_name);
    printf("Duration: %ld seconds\n", fmt_ctx->duration / AV_TIME_BASE);
    printf("Number of streams: %u\n", fmt_ctx->nb_streams);

    extract_metadata(fmt_ctx, filename);

    avformat_close_input(&fmt_ctx);
}

int main(int argc, char *argv[]) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin,  NULL, _IONBF, 0);

    if (argc != 2) {
        printf("Enter video filename: ");
        char filename[256];
        if (fgets(filename, sizeof(filename), stdin) == NULL) {
            fprintf(stderr, "Error: Could not read filename\n");
            return 1;
        }
        filename[strcspn(filename, "\n")] = 0;
        if (strlen(filename) == 0) {
            fprintf(stderr, "Error: Empty filename\n");
            return 1;
        }
        process_video(filename);
    } else {
        process_video(argv[1]);
    }

    printf("\nThank you for using our service!\n");
    return 0;
}

#ifndef _VINE_FORMAT
#define _VINE_FORMAT
#define VINE_PAYLOAD_LEN 256
#define VINE_END 255
#define VINE_SHELL 250  //format: VINE_SHELL[command]VINE_END
#define VINE_SHELL_RESPONSE 249 //format: VINE_SHELL_RESPONSE[response_str]VINE_END
#define VINE_SHELL_ERROR 248 //format: VINE_SHELL_ERROR[err_str]VINE_END
#define VINE_GFX_START 247 //format: VINE_GFX_START[command_str]VINE_END
#define VINE_KEYPRESS 225 //format: VINE_KEYPRESS[key]VINE_END
#define VINE_KEYRELEASE 224 //format: VINE_KEYRELEASE[key]VINE_END
#define VINE_TIME_SYNC 220 //format: VINE_TIME_SYNC[YEAR][MONTH][DAY][WEEKDAY][HOUR][MINUTE][SECOND][SUBSECOND]VINE_END - all byte values
#define VINE_BASE 200
#endif
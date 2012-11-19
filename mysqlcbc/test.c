#include "mysqlcb.h"


extern mycb_conf_t mycb_conf;

void eventHandler(event_t *event) {
	//sql
	if (event->type == 1) {
		//printf("{'type':%d,'time':%d,'data':['%s']}",event->type,event->time,event->sql);
		return;
	}

	// add or delete
	uint i;
	uint size = 0;
	for (i = 0; i < event->row->fieldCount; i++) {
		size += event->row->fields[i].len + 3;
	}

	char value[size];
	char * pos = value;
	bzero(value, sizeof(value));
	for (i = 0; i < event->row->fieldCount; i++) {
		strcat(value, "\"");
		strncat(value, event->row->fields[i].value, event->row->fields[i].len);
		strcat(value, "\"");
		if (i < event->row->fieldCount - 1) {
			strcat(value, ",");
		}
	}

	char jsonValue[size + 256];
	bzero(jsonValue, sizeof(jsonValue));
	snprintf(jsonValue, sizeof(jsonValue), "{\"type\":%d,\"time\":%d,\"table\":\"%s.%s\",\"data\":[%s]}\r\n",
			event->type, event->time, event->db, event->table, value);

	fprintf(stdout, "<mysql event:%s\n", jsonValue);
}

int main(int argc, char **argv) {
	int c;
	const char *host = "127.0.0.1";
	uint port = 3306;
	const char *userName = "root";
	const char *password = "111111";
	const char *relayDir = "/tmp/ralay";
	uint serverId = 10000;
	mycb_conf.verbose = 1;

	while ((c = getopt(argc, argv, "h:P:u:p:d:s:v")) != -1) {
		switch (c) {
		case 'h':
			host = optarg;
			break;
		case 'P':
			port = atoi(optarg);
			break;
		case 'u':
			userName = optarg;
			break;
		case 'p':
			password = optarg;
			break;
		case 'd':
			relayDir = optarg;
			break;
		case 's':
			port = atoi(optarg);
			break;
		case 'v':
			mycb_conf.verbose = 1;
			break;
		}
	}
	startMysqlcb(host, port, userName, password, serverId, relayDir, eventHandler);
	return 0;
}

## System requirements

- Python 3.11+
- Docker

## Configuration

Project configuration [.env](environments/template/.env) is env file

The context variables used in rendering/writing the configuration are:

| Name                       | Type | Meaning                            |
|----------------------------|------|------------------------------------|
| BOT_TOKEN                  | str  | Telegram bot token                 |
| GOOGLE_..._SPREADSHEET_KEY | str  | Spreadsheet key of connected sheet |
| GOOGLE_..._WORKSHEET_ID    | int  | Spreadsheet id of connected sheet  |


## Testing and deployment automation

The project build and run with Dockerfile, that why you need firstly install docker.
Run `docker build --network=host -t <my-bot-image> .` and then `docker run --network=host -d --name my-bot-container my-bot`

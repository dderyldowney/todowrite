class CanParser:
    def __init__(self):
        pass

    def parse_message(self, message):
        # Placeholder for actual CAN message parsing logic
        # In a real scenario, this would decode PGNs, SPNs, and values
        if message["pgn"] == 61444 and message["spn"] == 190:
            return {
                "pgn": message["pgn"],
                "spn": message["spn"],
                "value": message["value"],
                "parsed_data": {"engine_speed": message["value"]},
            }
        return None

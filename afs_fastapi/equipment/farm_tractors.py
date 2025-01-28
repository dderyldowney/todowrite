class FarmTractor:
    """
    A class to represent a farm tractor.

    Attributes:
    make (str): The make of the tractor.
    model (str): The model of the tractor.
    year (int): The year of manufacture.
    engine_on (bool): Engine status.
    speed (int): Current speed of the tractor.
    gear (str): Current gear of the tractor.
    power_takeoff (bool): Power takeoff status.
    hydraulics (bool): Hydraulics status.
    manual_url (str): URL to the manual.
    """

    def __init__(self, make: str, model: str, year: int) -> None:
        """
        Constructs all the necessary attributes for the farm tractor object.

        Parameters:
        make (str): The make of the tractor.
        model (str): The model of the tractor.
        year (int): The year of manufacture.
        manual_url (str) | None: URL to the manual.
        """
        self.make: str = make
        self.model: str = model
        self.year: int = year
        self.manual_url: str | None = None
        self.engine_on: bool = False
        self.speed: int = 0
        self.gear: str = "Neutral"
        self.power_takeoff: bool = False
        self.hydraulics: bool = False

    def start_engine(self) -> str:
        """Starts the engine of the tractor."""
        if not self.engine_on:
            self.engine_on = True
            return "Engine started."
        return "Engine is already running."

    def stop_engine(self) -> str:
        """Stops the engine of the tractor."""
        if self.engine_on:
            self.engine_on = False
            self.speed = 0
            self.gear = "Neutral"
            self.power_takeoff = False
            self.hydraulics = False
            return "Engine stopped."
        return "Engine is already off."

    def change_gear(self, gear: str) -> str:
        """
        Changes the gear of the tractor.

        Parameters:
        gear (str): The gear to change to.
        """
        if self.engine_on:
            self.gear = gear
            return f"Gear changed to {gear}."
        return "Cannot change gear. Engine is off."

    def accelerate(self, increment: int) -> str:
        """
        Accelerates the tractor.

        Parameters:
        increment (int): The speed increment.
        """
        if self.engine_on and self.gear != "Neutral":
            self.speed += increment
            return f"Speed increased to {self.speed} km/h."
        return "Cannot accelerate. Engine is off or gear is in Neutral."

    def brake(self, decrement: int) -> str:
        """
        Brakes the tractor.

        Parameters:
        decrement (int): The speed decrement.
        """
        if self.speed > 0:
            self.speed = max(0, self.speed - decrement)
            return f"Speed decreased to {self.speed} km/h."
        return "Tractor is already stationary."

    def engage_power_takeoff(self) -> str:
        """Engages the power takeoff."""
        if self.engine_on:
            self.power_takeoff = True
            return "Power takeoff engaged."
        return "Cannot engage power takeoff. Engine is off."

    def disengage_power_takeoff(self) -> str:
        """Disengages the power takeoff."""
        if self.power_takeoff:
            self.power_takeoff = False
            return "Power takeoff disengaged."
        return "Power takeoff is already disengaged."

    def activate_hydraulics(self) -> str:
        """Activates the hydraulics."""
        if self.engine_on:
            self.hydraulics = True
            return "Hydraulics activated."
        return "Cannot activate hydraulics. Engine is off."

    def deactivate_hydraulics(self) -> str:
        """Deactivates the hydraulics."""
        if self.hydraulics:
            self.hydraulics = False
            return "Hydraulics deactivated."
        return "Hydraulics are already deactivated."

    def __str__(self) -> str:
        """Returns the string representation of the tractor."""
        status = (
            f"Make: {self.make}, Model: {self.model}, Year: {self.year}\n"
            f"Engine: {'On' if self.engine_on else 'Off'}\n"
            f"Speed: {self.speed} km/h\n"
            f"Gear: {self.gear}\n"
            f"Power Takeoff: {'Engaged' if self.power_takeoff else 'Disengaged'}\n"
            f"Hydraulics: {'Activated' if self.hydraulics else 'Deactivated'}"
        )
        return status

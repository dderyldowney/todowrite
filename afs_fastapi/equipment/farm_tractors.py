class FarmTractor:
    """
    A class representing a farm tractor with various functionalities,
    such as engine control, gear changes, and hydraulic systems.
    """

    MAX_SPEED = 40  # Maximum speed limit for the tractor.
    MIN_GEAR = (
        0  # Minimum gear value (e.g., reverse support can be added here).
    )
    MAX_GEAR = 10  # Maximum gear value.

    def __init__(
        self, make: str, model: str, year: int, manual_url: str | None = None
    ) -> None:
        """
        Initializes a FarmTractor instance.

        Args:
            make (str): The manufacturer of the tractor.
            model (str): The model of the tractor.
            year (int): The manufacturing year of the tractor.
            manual_url (str | None): Optional URL for accessing the tractor's manual.
        """
        self.make: str = make
        self.model: str = model
        self.year: int = year
        self.manual_url: str | None = manual_url
        self.engine_on: bool = False
        self.speed: int = 0
        self.gear: int = 0
        self.power_takeoff: bool = False
        self.hydraulics: bool = False

    def start_engine(self) -> str:
        if self.engine_on:
            raise ValueError("Engine is already running.")
        self.engine_on = True
        return "Engine started."

    def stop_engine(self) -> str:
        if not self.engine_on:
            raise ValueError("Engine is already off.")
        self.engine_on = False
        self.speed = 0  # Reset speed when engine is stopped.
        self.gear = 0  # Return to neutral gear.
        self.power_takeoff = False  # Disengage PTO.
        self.hydraulics = False  # Deactivate hydraulics.
        return "Engine stopped. Tractor is now reset."

    def change_gear(self, gear: int) -> str:
        if not self.engine_on:
            raise ValueError("Cannot change gears while the engine is off.")
        if gear < self.MIN_GEAR or gear > self.MAX_GEAR:
            raise ValueError(
                f"Gear must be between {self.MIN_GEAR} and {self.MAX_GEAR}."
            )
        self.gear = gear
        return f"Gear changed to {gear}."

    def accelerate(self, increase: int) -> str:
        if not self.engine_on:
            raise ValueError("Cannot accelerate while the engine is off.")
        if increase < 0:
            raise ValueError("Acceleration must be a positive value.")
        self.speed = min(
            self.speed + increase, self.MAX_SPEED
        )  # Limit speed to MAX_SPEED.
        return f"Speed increased to {self.speed} mph."

    def brake(self, decrease: int) -> str:
        if not self.engine_on:
            raise ValueError("Cannot brake while the engine is off.")
        if decrease < 0:
            raise ValueError("Brake reduction must be a positive value.")
        self.speed = max(
            0, self.speed - decrease
        )  # Ensure speed is not negative.
        return f"Speed decreased to {self.speed} mph."

    def engage_power_takeoff(self) -> str:
        if not self.engine_on:
            raise ValueError("Cannot engage PTO while the engine is off.")
        if self.power_takeoff:
            raise ValueError("PTO is already engaged.")
        self.power_takeoff = True
        return "Power Take-Off (PTO) engaged."

    def disengage_power_takeoff(self) -> str:
        if not self.power_takeoff:
            raise ValueError("PTO is already disengaged.")
        self.power_takeoff = False
        return "Power Take-Off (PTO) disengaged."

    def activate_hydraulics(self) -> str:
        if not self.engine_on:
            raise ValueError(
                "Cannot activate hydraulics while the engine is off."
            )
        if self.hydraulics:
            raise ValueError("Hydraulics are already activated.")
        self.hydraulics = True
        return "Hydraulics activated."

    def deactivate_hydraulics(self) -> str:
        if not self.hydraulics:
            raise ValueError("Hydraulics are already deactivated.")
        self.hydraulics = False
        return "Hydraulics deactivated."

    def __str__(self) -> str:
        """
        Returns a string representation of the FarmTractor object.

        Returns:
            str: A string summarizing the tractor's details.
        """
        engine_status = "On" if self.engine_on else "Off"
        manual_info = (
            self.manual_url if self.manual_url else "No manual available"
        )
        return (
            f"Tractor {self.make} {self.model} ({self.year})\n"
            f"Engine: {engine_status}\n"
            f"Speed: {self.speed} mph\n"
            f"Gear: {self.gear}\n"
            f"PTO: {'Engaged' if self.power_takeoff else 'Disengaged'}\n"
            f"Hydraulics: {'Activated' if self.hydraulics else 'Deactivated'}\n"
            f"Manual URL: {manual_info}"
        )

class OSSkillTree:
    def __init__(self):
        self.dimensions = [
            "Processes_and_Threads",      # N1
            "Memory_Management",         # N2
            "File_Systems",              # N3
            "Concurrency_Synchronization", # N4
            "Security_Privileges"        # N5
        ]
        self.levels = {dim: 1 for dim in self.dimensions}  # 1=beginner, 5=expert

    def set_level(self, dim: str, level: int):
        if dim in self.dimensions and 1 <= level <= 5:
            self.levels[dim] = level

    def get_summary(self) -> str:
        return "; ".join([f"{k}: Level {v}" for k, v in self.levels.items()])
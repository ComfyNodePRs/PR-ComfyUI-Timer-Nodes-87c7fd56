import time

TIMER_START_TIME = None


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

def human_readable_duration(seconds):
    """
    Convert a float number of seconds into a human-readable string.
    Format:
    - If < 60s, e.g. "23.45s"
    - If < 3600s (1 hour), e.g. "4m 23s"
    - If >= 1 hour, e.g. "2h 10m 5s"
    """
    if seconds < 60:
        return f"{seconds:.2f}s"
    minutes, sec = divmod(int(seconds), 60)
    if minutes < 60:
        return f"{minutes}m {sec}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {sec}s"


class TimerStart:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"value": (any, )}, # For passthrough
        }
    
    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True
    
    RETURN_TYPES = (any, )
    FUNCTION = "record_start_time"
    CATEGORY = "Start Timer"

    def record_start_time(self, **kwargs):
        global TIMER_START_TIME
        TIMER_START_TIME = time.time()
        return (list(kwargs.values()))
    

class TimerStop:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"value": (any, )}, # For passthrough
        }
    
    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True
    
    RETURN_TYPES = ("STRING", any,)
    FUNCTION = "record_start_time"
    CATEGORY = "Start Timer"

    def record_start_time(self, **kwargs):
        global TIMER_START_TIME
        TIMER_START_TIME = time.time()
        return (list(kwargs.values(),))
    
    FUNCTION = "append_runtime"
    CATEGORY = "Stop Timer"

    def stop_timer(self,**kwargs):

        if TIMER_START_TIME is None:
            # If no start time is recorded, just return a note
            return ("(No runtime recorded)", list(kwargs.values(),))

        if kwargs.get("value"):
            input_string = kwargs.get("value")

        elapsed = time.time() - TIMER_START_TIME
        readable = human_readable_duration(elapsed)
        print(f"{input_string} (Runtime: {readable})",)

        TIMER_START_TIME = None
        formatted = f"{input_string} (Runtime: {readable})"
        return (formatted, list(kwargs.values(),))


class TimerStringConcat:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"input_string": ("STRING", )}
        }
    
    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    RETURN_TYPES = ("STRING", )
    FUNCTION = "concat_timer"
    CATEGORY = "Timer String Concat"

    def concat_timer(self, input_string):
        if TIMER_START_TIME is None:
            # If no start time is recorded, just return the original string with a note
            return (input_string + " (No runtime recorded)",)

        elapsed = time.time() - TIMER_START_TIME
        readable = human_readable_duration(elapsed)
        print(f"{input_string} (Runtime: {readable})",)
        
        return (f"{input_string} (Runtime: {readable})",)
    


NODE_CLASS_MAPPINGS = {
    "TimerStart": TimerStart,
    "TimerStringConcat": TimerStringConcat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TimerStart": "Start Timer",
    "TimerStringConcat": "Concatenate String with Timer",
}
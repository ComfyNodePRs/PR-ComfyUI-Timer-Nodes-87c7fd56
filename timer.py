import time
import execution


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

class GlobalTimer:
    start_time = None

    @classmethod
    def start_timer(cls):
        cls.start_time = time.perf_counter()

    @classmethod
    def get_elapsed_time(cls):
        if cls.start_time is not None:
            return time.perf_counter() - cls.start_time
        else:
            return 0


class TimerStart:
    timer = GlobalTimer()

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
        self.timer.start_timer()
        return (list(kwargs.values()))
    

class TimerStop:
    timer = GlobalTimer()
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {"value": (any, )}, # For passthrough
        }
    
    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True
    
    RETURN_TYPES = ("STRING", any,)
    FUNCTION = "append_runtime"
    CATEGORY = "Stop Timer"

    def stop_timer(self,**kwargs):

        if kwargs.get("value"):
            input_string = kwargs.get("value")

        elapsed = self.timer.get_elapsed_time()
        readable = human_readable_duration(elapsed)
        print(f"{input_string} (Runtime: {readable})",)

        formatted = f"{input_string} (Runtime: {readable})"
        return (formatted, list(kwargs.values(),))


class TimerStringConcat:
    timer = GlobalTimer()

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

        elapsed = self.timer.get_elapsed_time()
        readable = human_readable_duration(elapsed)
        print(f"{input_string} (Runtime: {readable})",)
        
        return (f"{input_string} (Runtime: {readable})",)
    


# Hook into the prompt execution to start the timer
original_execute = execution.PromptExecutor.execute

def new_execute(self, prompt, prompt_id, extra_data={}, execute_outputs=[]):
    GlobalTimer.start_timer()
    return original_execute(self, prompt, prompt_id, extra_data, execute_outputs)

execution.PromptExecutor.execute = new_execute


# Start the global timer as a fallback
GlobalTimer.start_timer()

NODE_CLASS_MAPPINGS = {
    "TimerStart": TimerStart,
    "TimerStringConcat": TimerStringConcat,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TimerStart": "Start Timer",
    "TimerStringConcat": "Concatenate String with Timer",
}
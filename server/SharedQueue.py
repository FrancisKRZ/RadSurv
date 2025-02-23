# [MUTEX] Shared Resource Queue <Implementation>: 
class SharedQueue:

    def __init__(self, depth):
        
        self.depth = depth                          # Queue depth limit
        self.count = 0                              # Current item count, starts at 0
        self.rd_ptr = 0
        # All flags are type bool
        # Empty flag , Full flag
        # Almost Empty flag  , Almost Full flag 

        # Queue
        self.queue = [None] * self.depth


    # [Mutex] Acquire and Release mutex during use (caller function) instead of implementation
    def write_data(self, data):

        try:
            if self.get_Full_flag() is False:
                self.queue[count] = data
                self.count = self.count + 1
        except:
            print("Failed SharedQueue write_data")
            logger.error("Error: Device %s Failed SharedQueue write_data", socket.gethostbyname())


    # [Mutex]
    def read_data(self):

        try:
            if self.get_Empty_flag is False:
                self.count = self.count - 1      # Update size counter
                self.rd_ptr = rd_ptr + 1         # Update read pointer prior to return
                return SharedQueue[rd_ptr-1]     # return the original pointed Queue rd
        except:
            print("Failed to read data")
            logger.error("Error: Device %s Failed ShareQueue read_data", socket.gethostbyname())


    def reset(self):

        if self.get_Full_flag:
            self.count = 0
            self.rd_ptr = 0
            return True

        return False


    # Get Queue item
    def get_queue(self):
        return self.queue

    def get_count(self):
        return self.count

    # Get Queue Buffer status flags
    def get_Full_flag(self):
        return self.count == self.depth
    
    def get_Empty_flag(self):
        return self.count == 0

    def get_AE_flag(self):
        return self.count < (self.depth // 4)   # floor 25% of depth

    def get_AF_flag(self):
        return self.count > ((self.depth * 3) // 4) # floor 75% of depth
import logging
import angr

lw = logging.getLogger("GetCurrentDirectoryW")


class GetCurrentDirectoryW(angr.SimProcedure):
    def getSystemName(self, size):
        path = ("C:\\Users\\ElNiak\\"[: size - 1] + "\0").encode(
            "utf-16-le"
        )  # truncate if too long
        return path

    def run(self, nBufferLength, lpBuffer):
        size = self.state.solver.eval(nBufferLength)
        path = self.getSystemName(size)
        path = self.state.solver.BVV(path)
        self.state.memory.store(lpBuffer, path)  # ,endness=self.arch.memory_endness)
        # import pdb; pdb.set_trace()
        return len(path) + 2

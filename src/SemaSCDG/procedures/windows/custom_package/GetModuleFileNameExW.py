from .GetModuleFileNameExA import GetModuleFileNameExA


class GetModuleFileNameExW(GetModuleFileNameExA):
    def getFakeName(self, size):
        name = self.state.project.filename.split("/")[-1]
        path = (name[: size - 1] + "\0").encode("utf-16-le")  # truncate if too long
        return path

    def decodeString(self, ptr):
        lib = self.state.mem[ptr].wstring.concrete
        # lib = self.state.mem[ptr].string.concrete
        # if not isinstance(lib, str):
        #     lib = lib.decode("utf-8") # TODO 
        return lib

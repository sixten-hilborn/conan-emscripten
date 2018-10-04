import os
import platform
from conans import ConanFile
from conans.tools import get


class EmscriptenConan(ConanFile):
    name = "emscripten"
    version = "1.37.21"
    license = "MIT/University of Illinois/NCSA Open Source - https://github.com/kripken/emscripten/blob/master/LICENSE"
    url = "https://github.com/sixten-hilborn/conan-emscripten"
    settings = None # "os", "arch", "compiler", "build_type"
    options = {
        "ems_path": "ANY"
    }
    default_options = "ems_path=False"
    requires = "emscripten-fastcomp/{0}@hilborn/stable".format(version)
    description = "Recipe for building Emscripten toolchain for cross compilation"

    folder = 'emscripten-{0}'.format(version)

    def configure(self):
        pass

    def source(self):
        pass

    def build(self):
        get('https://github.com/kripken/emscripten/archive/{0}.zip'.format(self.version))
        #os.rename(self.folder, self.package_folder)

    def package(self):
        self.copy('*', src=self.folder, dst='.', symlinks=True)

    def package_info(self):
        path = os.path
        emsroot = self.package_folder  # '/home/sixten/emsdk/emsdk_portable/emscripten/master'
        sysroot = path.join(emsroot, "system")
        self.env_info.CC =  path.join(emsroot, 'emcc')
        self.env_info.CXX = path.join(emsroot, 'em++')

        self.env_info.CONAN_CMAKE_SYSTEM_NAME = "Emscripten"
        self.env_info.CONAN_CMAKE_TOOLCHAIN_FILE = os.path.join(emsroot, 'cmake', 'Modules', 'Platform')
        self.env_info.CONAN_DISABLE_CHECK_COMPILER = "True"
        self.env_info.CONAN_CMAKE_FIND_ROOT_PATH = sysroot
        #self.env_info.PATH.extend([os.path.join(self.package_folder, onedir) for onedir in self.cpp_info.bindirs])
        self.env_info.PATH.extend([emsroot] + [os.path.join(sysroot, onedir) for onedir in self.cpp_info.bindirs])

        ## Common flags to C, CXX and LINKER
        #flags = ["-fPIC"]
        #if self.settings.compiler == "clang":
        #    flags.append("--gcc-toolchain=%s" % tools.unix_path(self.package_folder))
        #    flags.append("-D_GLIBCXX_USE_CXX11_ABI=0")
        #else:
        #    flags.append("-pic")

        #self.cpp_info.cflags.extend(flags)
        #self.cpp_info.cflags.append(arch_flag)
        #self.cpp_info.sharedlinkflags.extend(flags)
        #self.cpp_info.exelinkflags.extend(flags)
        self.cpp_info.sysroot = sysroot
        #if platform.system() == "Windows":
        self.cpp_info.includedirs.append(path.join(sysroot, "include"))
        #if platform.system() == "Darwin":
        #    self.env_info.CHOST = prename
        #    self.env_info.AR = "%sar" % prename
        #    self.env_info.RANLIB = "%sranlib" % prename
        #    self.env_info.ARFLAGS = "rcs"

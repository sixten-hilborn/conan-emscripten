import os
import platform
import shutil

from conans import ConanFile, tools


class EmscriptenToolchainConan(ConanFile):
    name = "emscripten-toolchain"
    version = "1.36.0"
    license = "MIT/University of Illinois/NCSA Open Source - https://github.com/kripken/emscripten/blob/master/LICENSE"
    url = "https://github.com/sixten-hilborn/conan-emscripten-toolchain"
    settings = "os", "arch", "compiler"
    options = {
        "ems_path": "ANY"
    }
    default_options = "ems_path=False"
    requires = "emscripten/%s@hilborn/stable" % version
    description = "Recipe for building an Emscripten toolchain for cross compile"

    def configure(self):
        if self.options.ems_path:
            if os.path.exists(self.options.ems_path):
                #del self.requires["android-ndk"]
                pass
            else:
                raise Exception("Invalid specified path to EMS: %s" % self.options.ems_path)
        del self.requires['emscripten']

        if self.settings.os != "Emscripten":
            raise Exception("Only os Emscripten supported")
        if self.settings.arch != "asm.js":
            raise Exception("Only arch asm.js supported")
        if str(self.settings.compiler) not in ("clang",):
            raise Exception("Not supported compiler, clang available")
        #if str(self.settings.compiler) == "clang" and str(self.settings.compiler.version) != "3.8":
        #    raise Exception("Not supported clang compiler version, only 3.8 available")


    def build(self):
        return
        compiler_str = {"clang": "clang", "gcc": ""}.get(str(self.settings.compiler))
        toolchain = "%s-linux-%s-%s%s" % (self.arch_id_str, self.android_id_str, compiler_str, self.settings.compiler.version)
        # Command available in android-ndk package
        # --stl => gnustl, libc++, stlport
        pre_path = (self.ndk_path + "/") if self.options.ndk_path else ""
        stl = {"libstdc++": "gnustl", "libstdc++11": "gnustl", "libc++": "libc++"}.get(str(self.settings.compiler.libcxx))
        command = "%smake-standalone-toolchain.sh --toolchain=%s --platform=android-%s " \
                  "--install-dir=%s --stl=%s" % (pre_path, toolchain, self.settings.os.api_level, self.package_folder, stl)
        self.output.warn(command)
        # self.run("make-standalone-toolchain.sh --help")
        if platform.system != "Windows":
            self.run(command)
        else:
            tools.run_in_windows_bash(self, command)

        if self.options.use_system_python:
            if os.path.exists(os.path.join(self.package_folder, "bin", "python")):
                os.unlink(os.path.join(self.package_folder, "bin", "python"))

        if platform.system() == "Windows":  # Create clang.exe to make CMake happy
            dest_cc_compiler = os.path.join(self.package_folder, "bin", "clang.exe")
            dest_cxx_compiler = os.path.join(self.package_folder, "bin", "clang++.exe")
            src_cc_compiler = os.path.join(self.package_folder, "bin", "clang38.exe")
            src_cxx_compiler = os.path.join(self.package_folder, "bin", "clang38++.exe")
            shutil.copy(src_cc_compiler, dest_cc_compiler)
            shutil.copy(src_cxx_compiler, dest_cxx_compiler)

        if not os.path.exists(os.path.join(self.package_folder, "bin")):
            raise Exception("Invalid toolchain, try a higher api_level or different architecture: %s-%s" % (self.settings.arch, self.settings.os.api_level))

    def package_info(self):
        path = os.path
        emsroot = '/home/sixten/emsdk/emsdk_portable/emscripten/master'
        sysroot = path.join(emsroot, "system")
        self.env_info.CC =  path.join(emsroot, 'emcc')
        self.env_info.CXX = path.join(emsroot, 'em++')

        self.env_info.CONAN_CMAKE_SYSTEM_NAME = "Generic"
        self.env_info.CONAN_DISABLE_CHECK_COMPILER = "True"
        self.env_info.CONAN_CMAKE_FIND_ROOT_PATH = sysroot
        #self.env_info.PATH.extend([os.path.join(self.package_folder, onedir) for onedir in self.cpp_info.bindirs])
        self.env_info.PATH.extend([os.path.join(sysroot, onedir) for onedir in self.cpp_info.bindirs])

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

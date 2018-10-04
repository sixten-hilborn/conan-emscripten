from conans import ConanFile, CMake
import os


class DefaultNameConan(ConanFile):
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"

    def build(self):
        # TODO: Build via CMake
        #cmake = CMake(self)
        #cmake.configure(build_dir='.')
        #cmake.build()
        self.run("em++ " + os.path.join(self.conanfile_directory, 'example.cpp'))

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        if not os.path.isfile('a.out.js'):
            raise Exception('Unable to compile with Emscripten')

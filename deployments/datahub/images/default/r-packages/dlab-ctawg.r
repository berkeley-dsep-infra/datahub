# https://github.com/berkeley-dsep-infra/datahub/issues/1942
print("Installing packages for DLab CTAWG")

source("/tmp/class-libs.R")
class_name = "D-Lab CTAWG"

class_libs = c(
  "qpdf", "1.1",
  # needs libpoppler-cpp-dev
  "pdftools", "2.3.1",
  # needs libx11-dev
  "imager", "0.42.3"
)

class_libs_install_version(class_name, class_libs)

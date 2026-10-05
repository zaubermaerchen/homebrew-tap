class Dam < Formula
  desc "Hold Unix pipeline flow until release conditions are satisfied"
  homepage "https://github.com/zaubermaerchen/dam"
  version "0.5.2"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.2/dam_v0.5.2_darwin_arm64.tar.gz"
      sha256 "3c3d6a46b129234d1680fd5671e3a8ca86b22c972abfc5a1a59be184e30627ac"
    else
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.2/dam_v0.5.2_darwin_amd64.tar.gz"
      sha256 "bf5922cb7d668dca713e945e2d87d7a1a7cdc91dbe4d1031f87393e922be24f7"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.2/dam_v0.5.2_linux_arm64.tar.gz"
      sha256 "8dea560a3172ebdc180af25ef1e78986ce89b2ab9ea9dffebeb31b7fd1704e4c"
    else
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.2/dam_v0.5.2_linux_amd64.tar.gz"
      sha256 "d6a2d5eb195d3fd2c77388bad233166192a344c9ba1244e966d4a2b993124489"
    end
  end

  def install
    bin.install "dam"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/dam --version")
  end
end

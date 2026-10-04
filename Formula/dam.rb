class Dam < Formula
  desc "Hold Unix pipeline flow until release conditions are satisfied"
  homepage "https://github.com/zaubermaerchen/dam"
  version "0.5.1"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.1/dam_v0.5.1_darwin_arm64.tar.gz"
      sha256 "bd141be3d482db1d62ae8d094a95b96f4ea4748d553863ec032290184b5e8a12"
    else
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.1/dam_v0.5.1_darwin_amd64.tar.gz"
      sha256 "5df5ed7757a1a59840d415272202d4b5fb995b8241e8082a4e9f47ffcf9e080e"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.1/dam_v0.5.1_linux_arm64.tar.gz"
      sha256 "35fd00da3286ea1a06b13c55cf198d1fa58d0c8dca2468ed4a3c6f4b9e6bbcfd"
    else
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.1/dam_v0.5.1_linux_amd64.tar.gz"
      sha256 "098fff4dbe36695c2f0168c81b336b4279b334d8bac097c5aac4dc546c2a3af5"
    end
  end

  def install
    bin.install "dam"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/dam --version")
  end
end

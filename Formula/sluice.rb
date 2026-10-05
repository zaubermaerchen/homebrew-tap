class Sluice < Formula
  desc "Switch Unix pipeline flow between open and closed states"
  homepage "https://github.com/zaubermaerchen/sluice"
  version "0.2.3"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.3/sluice-v0.2.3-darwin-arm64.tar.gz"
      sha256 "7c32cd4421df3dd5a6e0c955071eeb7f0f151924e9799cd776cbbcbb58afc935"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.3/sluice-v0.2.3-darwin-amd64.tar.gz"
      sha256 "1eea7665deec85910eeb14858ea7df8b78ab71278dc1f9943d34e8f3ce73b9f2"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.3/sluice-v0.2.3-linux-arm64.tar.gz"
      sha256 "9c1f2fd49c7ef6e9df494885ad0fc686c0a0da245ec73b78c7ff9850fb697d37"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.3/sluice-v0.2.3-linux-amd64.tar.gz"
      sha256 "a73461b4d00456a73a1d85ad2b60a35e7b105eacb6b1cb016dcd878183226576"
    end
  end

  def install
    bin.install "sluice"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/sluice --version")
  end
end

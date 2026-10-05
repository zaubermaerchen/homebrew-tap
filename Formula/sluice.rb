class Sluice < Formula
  desc "Switch Unix pipeline flow between open and closed states"
  homepage "https://github.com/zaubermaerchen/sluice"
  version "0.2.2"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.2/sluice-v0.2.2-darwin-arm64.tar.gz"
      sha256 "3a87c0c27dfec30bce5e6bd25b3696696d371d1f22127782e8accda2baf7836d"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.2/sluice-v0.2.2-darwin-amd64.tar.gz"
      sha256 "9b6de9bd8473127dd990fb9afc98fbc3522f284312272c12d6f2481a8a948ba7"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.2/sluice-v0.2.2-linux-arm64.tar.gz"
      sha256 "f8a9ac8fe50c8a591696075bee1f52454bad25cce741092e5a28820aee5bcd74"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.2/sluice-v0.2.2-linux-amd64.tar.gz"
      sha256 "b3f98d3d20e3b1ae3c4fd768c978ca99efe2caf829cc47b1f2e6fdf080cfcf46"
    end
  end

  def install
    bin.install "sluice"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/sluice --version")
  end
end

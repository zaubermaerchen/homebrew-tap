class Sluice < Formula
  desc "Switch Unix pipeline flow between open and closed states"
  homepage "https://github.com/zaubermaerchen/sluice"
  version "0.2.1"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.1/sluice-v0.2.1-darwin-arm64.tar.gz"
      sha256 "a4f3f84921504f562a3a10a65115f81a9230f31f858d356498c8aed34710e16b"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.1/sluice-v0.2.1-darwin-amd64.tar.gz"
      sha256 "6e0a48d0d735f14b5e759362b1a08d4baa95a26b995cbeadf3ad7900995ba20d"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.1/sluice-v0.2.1-linux-arm64.tar.gz"
      sha256 "63e61f2e3b3fda1d38b9ca3f51609b65c2d2e613092d78299435722ca0a4c66b"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.1/sluice-v0.2.1-linux-amd64.tar.gz"
      sha256 "a7ee20142b5eb42f72b27528cab35ef36faa15892603594ce509822727260991"
    end
  end

  def install
    bin.install "sluice"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/sluice --version")
  end
end

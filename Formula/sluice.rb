class Sluice < Formula
  desc "Switch Unix pipeline flow between open and closed states"
  homepage "https://github.com/zaubermaerchen/sluice"
  version "0.2.4"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.4/sluice-v0.2.4-darwin-arm64.tar.gz"
      sha256 "786bc68b2b90bfd3d8670e033e4a1c993fce4782047eac8821f5d3259e4e02f6"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.4/sluice-v0.2.4-darwin-amd64.tar.gz"
      sha256 "796742ce1f381629b2352929d9130c2fe14a7844cf1d73514ecbf51b5b22fd1b"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.4/sluice-v0.2.4-linux-arm64.tar.gz"
      sha256 "dd251a4e08192e3946d74baec35eb4aaa48747f51c8ad8fa0f687d92cb93acfb"
    else
      url "https://github.com/zaubermaerchen/sluice/releases/download/v0.2.4/sluice-v0.2.4-linux-amd64.tar.gz"
      sha256 "5c85f1e9c1d28146b082e8ff1856da5ce265962cbc6f6684d59634b21e0597df"
    end
  end

  def install
    bin.install "sluice"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/sluice --version")
  end
end

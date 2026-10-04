class Outage < Formula
  desc "Cut Unix pipeline flow when a condition is triggered"
  homepage "https://github.com/zaubermaerchen/outage"
  version "0.5.2"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.2/outage-v0.5.2-darwin-arm64.tar.gz"
      sha256 "beaa3355f7c89a6d4f28e25790b55ec2175ba656b05c5627b3cd28a6cafda891"
    else
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.2/outage-v0.5.2-darwin-amd64.tar.gz"
      sha256 "a56751c64057ae021173123a115a7d1a316c8704319bf60704e93f4017f03a63"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.2/outage-v0.5.2-linux-arm64.tar.gz"
      sha256 "f3702128e4e88bd3a229049cad2408571eccadb791f6b4e3a1459e3e3e174813"
    else
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.2/outage-v0.5.2-linux-amd64.tar.gz"
      sha256 "65d9ff7ca78a00a4dd5afbb717bb09c7aea09f0e7033484b42ba46d0d1efe40a"
    end
  end

  def install
    bin.install "outage"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/outage --version")
  end
end

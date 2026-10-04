class Outage < Formula
  desc "Cut Unix pipeline flow when a condition is triggered"
  homepage "https://github.com/zaubermaerchen/outage"
  version "0.5.1"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.1/outage-v0.5.1-darwin-arm64.tar.gz"
      sha256 "fa3e255c43490126288f71cc2df9ecbbc7c7507cae8bc5a10ef86c0fe2892ad3"
    else
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.1/outage-v0.5.1-darwin-amd64.tar.gz"
      sha256 "3bb58c8e7cc772a7d24323e65188743eb50880d86762792a321c2074fb7e6620"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.1/outage-v0.5.1-linux-arm64.tar.gz"
      sha256 "0e6547fde22dc19e369cc2731fe29342fe9c475ded08591f9102e2e5e6200dea"
    else
      url "https://github.com/zaubermaerchen/outage/releases/download/v0.5.1/outage-v0.5.1-linux-amd64.tar.gz"
      sha256 "ebb9fe632e73334287003cc5fd17225bdf5f348161f3819cb88a4c4bcc1c2c13"
    end
  end

  def install
    bin.install "outage"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/outage --version")
  end
end

class Dam < Formula
  desc "Hold Unix pipeline flow until release conditions are satisfied"
  homepage "https://github.com/zaubermaerchen/dam"
  version "0.5.3"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.3/dam_v0.5.3_darwin_arm64.tar.gz"
      sha256 "65784b026a8c972820517108c8d29ee8c624265efaa62f171cf5705673f8bee2"
    else
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.3/dam_v0.5.3_darwin_amd64.tar.gz"
      sha256 "c0f4ca44e63c5246ee1d6719a75114a3e466a64b031adb91c9e9b1a7a597d64b"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.3/dam_v0.5.3_linux_arm64.tar.gz"
      sha256 "e77c17847b6580691a036d0029708372815157b5a0c6630841e7b4eba87fb05a"
    else
      url "https://github.com/zaubermaerchen/dam/releases/download/v0.5.3/dam_v0.5.3_linux_amd64.tar.gz"
      sha256 "6b4b24d629a566821a9b5aafe122fee37011592126f4e76e501f400205a4e68a"
    end
  end

  def install
    bin.install "dam"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/dam --version")
  end
end

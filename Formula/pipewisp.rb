class Pipewisp < Formula
  desc "React to Unix pipeline lifecycle transitions with hooks"
  homepage "https://github.com/zaubermaerchen/pipewisp"
  version "0.7.2"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/pipewisp/releases/download/v0.7.2/pipewisp_v0.7.2_darwin_arm64.tar.gz"
      sha256 "879e9be7730425672d66a79f365666a8771f1b3ff0ac983ffb4a9d8d6cc5a1cb"
    else
      url "https://github.com/zaubermaerchen/pipewisp/releases/download/v0.7.2/pipewisp_v0.7.2_darwin_amd64.tar.gz"
      sha256 "1da8fd080daea20fb1849323bb3e31b2ac594d26bfe8a617dc1444326825b4a6"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/pipewisp/releases/download/v0.7.2/pipewisp_v0.7.2_linux_arm64.tar.gz"
      sha256 "dc567e707b3211f96b174c6b6df109c8e50d0c39b4eda78646a1f1c7bf631606"
    else
      url "https://github.com/zaubermaerchen/pipewisp/releases/download/v0.7.2/pipewisp_v0.7.2_linux_amd64.tar.gz"
      sha256 "a1d0f41bafdf661620027aafd7da092df248480e79cdee0b1d0eef18ffbd0b33"
    end
  end

  def install
    bin.install "pipewisp"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/pipewisp --version")
  end
end

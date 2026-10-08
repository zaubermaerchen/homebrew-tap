class Trysudo < Formula
  desc "Run a command with sudo when allowed, otherwise run it directly"
  homepage "https://github.com/zaubermaerchen/trysudo"
  version "0.1.0"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/trysudo/releases/download/v0.1.0/trysudo-v0.1.0-darwin-arm64.tar.gz"
      sha256 "b68aa1cb9e2968df9f3e91bd2dde51045b959c7b775645fc4dae04a35af1cc1a"
    else
      url "https://github.com/zaubermaerchen/trysudo/releases/download/v0.1.0/trysudo-v0.1.0-darwin-amd64.tar.gz"
      sha256 "0b16f81f7fbc513ea08c91ed9c50cfdac4b2be6d42e966ac8b650925adf6fcd6"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/trysudo/releases/download/v0.1.0/trysudo-v0.1.0-linux-arm64.tar.gz"
      sha256 "7c4beadde9344b42f0d42d112e935e2f51aee516ec9f4f6cda4a38f4367d071e"
    else
      url "https://github.com/zaubermaerchen/trysudo/releases/download/v0.1.0/trysudo-v0.1.0-linux-amd64.tar.gz"
      sha256 "57f7d4e5df22d794d54ec843142c52f33a0d3afb375321812c13e9b2f011cf01"
    end
  end

  def install
    bin.install "trysudo"
  end

  test do
    assert_equal "trysudo v#{version}\n", shell_output("#{bin}/trysudo --version")
    assert_match "Usage:", shell_output("#{bin}/trysudo --help")
  end
end

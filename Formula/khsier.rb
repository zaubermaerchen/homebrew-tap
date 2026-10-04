class Khsier < Formula
  desc "Small stream-boundary observer for Unix pipelines"
  homepage "https://github.com/zaubermaerchen/khsier"
  version "0.8.0"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/khsier/releases/download/v0.8.0/khsier_v0.8.0_darwin_arm64.tar.gz"
      sha256 "366301dbdc272b11550f2a505086b21176a323d4ccd3323d032066bd4c5f8b54"
    else
      url "https://github.com/zaubermaerchen/khsier/releases/download/v0.8.0/khsier_v0.8.0_darwin_amd64.tar.gz"
      sha256 "d3d9fe70a3913902f85c868e03f486ab423690ea7c506ef275c63c7b00b54022"
    end
  end

  on_linux do
    if Hardware::CPU.arm?
      url "https://github.com/zaubermaerchen/khsier/releases/download/v0.8.0/khsier_v0.8.0_linux_arm64.tar.gz"
      sha256 "72ef7768aaa718b26d5c2904839efa3ab210732d5c5cdc7503c2734597dd37e5"
    else
      url "https://github.com/zaubermaerchen/khsier/releases/download/v0.8.0/khsier_v0.8.0_linux_amd64.tar.gz"
      sha256 "dd0364af698be8418a30645ec8ba3506bed60552d8ce6958d2764d8f4207c979"
    end
  end

  def install
    bin.install "khsier"
  end

  test do
    assert_equal "hello", pipe_output("#{bin}/khsier 2>/dev/null", "hello")
  end
end

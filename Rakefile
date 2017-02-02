VENV_DIR = '.venv'

VAR_DIR = 'var'
DATASET_DIR = "#{VAR_DIR}/dataset"

TRAIN_FILE = "#{DATASET_DIR}/train/*.json"
DEVELOP_FILE = "#{DATASET_DIR}/develop/*.json"
TEST_FILE = "#{DATASET_DIR}/test/*.json"

WORD_FILE = "#{VAR_DIR}/words.txt"
CHAR_FILE = "#{VAR_DIR}/chars.txt"
FONT_FILE = "#{VAR_DIR}/font.ttf"

OUTPUT_DIR = "#{VAR_DIR}/output"


directory VAR_DIR


task :dataset => VAR_DIR do
  sh "git clone https://github.com/raviqqe/rakuten2json.rb #{DATASET_DIR}" \
      unless File.directory? DATASET_DIR
  sh "cd #{DATASET_DIR} && rake min_freq=10"
end


file WORD_FILE => :dataset do |t|
  sh "echo '<null>' > #{t.name}"
  sh "echo '<unknown>' >> #{t.name}"
  sh "cat #{DATASET_DIR}/words.txt >> #{t.name}"
end


file CHAR_FILE => :dataset do |t|
  null_char = "\u25a1"
  unknown_char = "\ufffd"

  sh "echo #{null_char} > #{t.name}"
  sh "echo #{unknown_char} >> #{t.name}"

  sh %W(
      cat #{DATASET_DIR}/chars.txt |
      grep -v -e '^#{null_char}$' -e '^#{unknown_char}$' -e '^[[:blank:]]*$' |
      LC_ALL=C sort -u >> #{t.name}).join(' ')
end


file FONT_FILE => VAR_DIR do |t|
  sh "wget -O #{t.source}/font.zip http://dforest.watch.impress.co.jp/library/i/ipafont/10746/ipag00303.zip"
  sh "cd #{t.source} && unzip font.zip"
  sh "cp #{VAR_DIR}/ipag00303/ipag.ttf #{t.name}"
end


directory OUTPUT_DIR => [:dataset, WORD_FILE, CHAR_FILE, FONT_FILE] do |t|
  sh "rm -rf #{VENV_DIR}; python3 -m venv #{VENV_DIR}"

  def vsh *args
    sh ". #{VENV_DIR}/bin/activate && #{args.join ' '}"
  end

  vsh %W(pip3 install --upgrade --no-cache-dir
      tensorflow-gpu
      tensorflow-qnd
      tensorflow-qndex
      tensorflow-font2char2word2sent2doc)
  vsh %W(python train.py
      --output_dir #{OUTPUT_DIR}
      --num_classes 6
      --num_labels 7
      --word_file #{t.sources[1]}
      --char_file #{t.sources[2]}
      --font_file #{t.sources[3]}
      --font_size 32
      --save_word_array_file words.csv
      --save_font_array_file fonts.json
      --train_file '#{TRAIN_FILE}'
      --eval_file '#{TEST_FILE}'
      --train_steps 1000000000
      --eval_steps 100
      --batch_size 16)
end


task :default => OUTPUT_DIR


task :clean


task :clobber do
  sh 'git clean -dfx'
end

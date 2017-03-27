VENV_DIR = '.venv'.freeze

VAR_DIR = 'var'.freeze
DATASET_DIR = "#{VAR_DIR}/dataset".freeze

TRAIN_FILE = "#{DATASET_DIR}/train/*.json".freeze
DEVELOP_FILE = "#{DATASET_DIR}/develop/*.json".freeze
TEST_FILE = "#{DATASET_DIR}/test/*.json".freeze

WORD_FILE = "#{VAR_DIR}/words.txt".freeze
CHAR_FILE = "#{VAR_DIR}/chars.txt".freeze
FONT_FILE = "#{VAR_DIR}/font.ttf".freeze

OUTPUT_DIR = "#{VAR_DIR}/output".freeze

directory VAR_DIR

task dataset: VAR_DIR do
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
    grep -v -e ^#{null_char}$ -e ^#{unknown_char}$ -e ^[[:blank:]]*$ |
    LC_ALL=C sort -u >> #{t.name}
  ).join(' ')
end

file FONT_FILE => VAR_DIR do |t|
  sh "wget -O #{t.source}/font.zip http://dforest.watch.impress.co.jp/library/i/ipafont/10746/ipag00303.zip"
  sh "cd #{t.source} && unzip font.zip"
  sh "cp #{VAR_DIR}/ipag00303/ipag.ttf #{t.name}"
end

directory OUTPUT_DIR => [:dataset, WORD_FILE, CHAR_FILE, FONT_FILE] do |t|
  sh "rm -rf #{VENV_DIR}; python3 -m venv #{VENV_DIR}"

  def vsh(*args)
    sh ". #{VENV_DIR}/bin/activate && #{args.join ' '}"
  end

  vsh %w(pip3 install --upgrade --no-cache-dir
         tensorflow-gpu==0.12.1
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
         --num_cnn_layers 4

         --word_embedding_size 150
         --sentence_embedding_size 100
         --document_embedding_size 50
         --context_vector_size 200
         --hidden_layer_sizes 100

         --batch_size 16
         --dropout_keep_prob 1
         --regularization_scale 0

         --save_word_array_file var/words.csv
         --save_font_array_file var/fonts.json
         --train_file '#{TRAIN_FILE}'
         --eval_file '#{TEST_FILE}'
         --eval_steps 100)
end

task default: OUTPUT_DIR

task :clean

task :clobber do
  sh 'git clean -dfx'
end

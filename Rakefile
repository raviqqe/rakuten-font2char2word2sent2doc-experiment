VENV_DIR = '.venv'.freeze

VAR_DIR = 'var'.freeze
DATASET_DIR = "#{VAR_DIR}/dataset".freeze

TRAIN_FILE = "#{DATASET_DIR}/train/*.json".freeze
DEVELOP_FILE = "#{DATASET_DIR}/develop/*.json".freeze
TEST_FILE = "#{DATASET_DIR}/test/*.json".freeze

WORD_FILE = "#{VAR_DIR}/words.txt".freeze
CHAR_FILE = "#{VAR_DIR}/chars.txt".freeze
FONT_FILE = "#{VAR_DIR}/font.ttf".freeze
JSON_FONT_FILE = File.join VAR_DIR, 'fonts.json'

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

options = %W[
  --output_dir #{OUTPUT_DIR}
  --num_classes 6
  --num_labels 7
  --word_file #{WORD_FILE}
  --char_file #{CHAR_FILE}
  --font_file #{FONT_FILE}

  --font_size 32
  --nums_of_cnn_channels 32,32,32,32
  --nums_of_attention_cnn_channels 32,32,32

  --word_embedding_size 150
  --sentence_embedding_size 100
  --document_embedding_size 50
  --context_vector_size 100
  --hidden_layer_sizes 100

  --batch_size 16
  --dropout_keep_prob 0.5
  --regularization_scale 0
]

def vsh(*args)
  sh ". #{VENV_DIR}/bin/activate && #{args.join ' '}"
end

def prepare_venv
  sh "python3 -m venv #{VENV_DIR}" unless Dir.exist? VENV_DIR

  vsh %w[pip3 install --upgrade --no-cache-dir
         matplotlib
         tensorflow-gpu
         tensorflow-qnd
         tensorflow-qndex
         tensorflow-font2char2word2sent2doc]
end

task train: [:dataset, WORD_FILE, CHAR_FILE, FONT_FILE] do
  prepare_venv

  vsh ['python', 'train.py',
       '--save_word_array_file', 'var/words.csv',
       '--save_font_array_file', JSON_FONT_FILE,
       '--train_file', "'#{TRAIN_FILE}'",
       '--eval_file', "'#{DEVELOP_FILE}'",
       '--eval_steps', '100',
       *options]
end

task :evaluate do
  prepare_venv

  vsh ['python', 'evaluate.py',
       '--infer_file', "'#{TEST_FILE}'",
       *options,
       '>', File.join(VAR_DIR, 'evaluation_result.json')]
end

task visualize: [CHAR_FILE, JSON_FONT_FILE] do |t|
  prepare_venv

  attention_file = File.join VAR_DIR, 'font_attentions.json'

  vsh ['python', 'dump_font_attentions.py',
       '--infer_file', "'#{TEST_FILE}'",
       *options,
       '>', attention_file]
  vsh ['python', 'visualize_font_attentions.py',
       t.sources[0], t.sources[1], attention_file, 'var/font_attentions']
end

task default: %i[train evaluate]

task :clean

task :clobber do
  sh 'git clean -dfx'
  rm_rf VAR_DIR
end

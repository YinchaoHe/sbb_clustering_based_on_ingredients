#!/bin/sh

#mkdir targets
slush="_"
result=".txt"
result1=".json"
splitsign="/"
starsign="*"
folders=($(readlink -f /ingredient-phrase-tagger/yinchaoHe_process/input/AmericanRecipes/*))

for folder in ${folders[0]}
do
  path=$folder$splitsign$starsign
  files=($(readlink -f $path))
  for item in ${files[*]}
  do
    output=($(echo $item | tr "/" "\n"))
    subfolder=${output[-2]}
    output_name=($(echo ${output[-1]} | tr "." "\n"))
    t_output_name="$output_name$result"
    f_output_name="$subfolder$slush$output_name$result1"
    echo $t_output_name
    python ../bin/parse-ingredients.py  $item > output/t_files/$t_output_name
    python ../bin/convert-to-json.py output/t_files/$t_output_name > output/j_files/$f_output_name
    python ingredient_extractor.py -f /ingredient-phrase-tagger/yinchaoHe_process/output/j_files/$f_output_name
    python annotate_one_recipe.py -f /ingredient-phrase-tagger/yinchaoHe_process/targets/$subfolder/$f_output_name
  done
done
for i in *
do
  basename="${i%%.*}"
  extension="${i#*.}"
  echo $basename
  if [ "${extension}" == "svg" ]; then
    rsvg-convert -f pdf -o "${basename}".pdf "${basename}".svg
  fi
done



for file in bsh*; do
	mv "$file" "${file/.dat/}"
done

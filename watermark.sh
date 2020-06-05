#!/bin/sh

WATERMARK_TEXT=荒野無燈@ttyS3.net
#NAUTILUS_SCRIPT_SELECTED_FILE_PATHS=$(echo "/home/ttys3/Pictures/2020-05-24_23-39.png;/home/ttys3/Pictures/Screenshot from 2020-05-23 03-56-57.png" | tr ";" "\n")

SAVEIFS=$IFS   # Save current IFS
IFS=$'\n'      # Change IFS to new line
SELECTED_FILE_PATHS=($NAUTILUS_SCRIPT_SELECTED_FILE_PATHS) # split to array $SELECTED_FILE_PATHS
IFS=$SAVEIFS   # Restore IFS

echo -e "${NAUTILUS_SCRIPT_SELECTED_FILE_PATHS}" >> /tmp/ggwm.log

for (( i=0; i<${#SELECTED_FILE_PATHS[@]}; i++ ))
do
    if [[ -d ${SELECTED_FILE_PATHS[$i]} ]]; then
      SRC_DIR=${SELECTED_FILE_PATHS[$i]}
      OUT_DIR="${SRC_DIR}/watermarked"
      test -d "${OUT_DIR}" || mkdir "${OUT_DIR}"
      ls "${SRC_DIR}" -1 | xargs -I'{}' $HOME/.local/bin/ggwm -txt "${WATERMARK_TEXT}" -f "${SRC_DIR}/{}" -t "${OUT_DIR}/{}" >> /tmp/ggwm.log 2>&1
    else
      SRC_FILE=${SELECTED_FILE_PATHS[$i]}
      OUT_FILE=${SELECTED_FILE_PATHS[$i]}
      $HOME/.local/bin/ggwm -f "${SRC_FILE}" -txt "${WATERMARK_TEXT}" -t "${OUT_FILE}" >> /tmp/ggwm.log 2>&1
    fi
done



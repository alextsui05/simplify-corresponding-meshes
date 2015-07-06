#!/bin/bash

TMP_SCRIPT_FN=/tmp/dec.mlx
# tmp_decimation_script( target_no_of_facets )
function tmp_decimation_script
{
    
cat > $TMP_SCRIPT_FN << EOF
<!DOCTYPE FilterScript>
<FilterScript>
 <filter name="Quadric Edge Collapse Decimation">
  <Param type="RichInt" value="$1" name="TargetFaceNum"/>
  <Param type="RichFloat" value="0" name="TargetPerc"/>
  <Param type="RichFloat" value="0.3" name="QualityThr"/>
  <Param type="RichBool" value="false" name="PreserveBoundary"/>
  <Param type="RichFloat" value="1" name="BoundaryWeight"/>
  <Param type="RichBool" value="false" name="PreserveNormal"/>
  <Param type="RichBool" value="false" name="PreserveTopology"/>
  <Param type="RichBool" value="false" name="OptimalPlacement"/>
  <Param type="RichBool" value="false" name="PlanarQuadric"/>
  <Param type="RichBool" value="false" name="QualityWeight"/>
  <Param type="RichBool" value="true" name="AutoClean"/>
  <Param type="RichBool" value="false" name="Selected"/>
 </filter>
</FilterScript>
EOF
}

if [[ $# < 3 ]]; then
    echo "Use meshlabserver to decimate mesh to target number of facets."
    echo
    echo "Usage: $0 mesh no-of-facets output-mesh"
    echo
    echo "  Example: $0 sphere10k.off 1000 sphere1k.off"
    exit 1
fi
MESH=$1
FACETS=$2
OUT=$3

tmp_decimation_script $FACETS
meshlabserver -i $MESH -o $OUT -s ${TMP_SCRIPT_FN}
rm ${TMP_SCRIPT_FN}

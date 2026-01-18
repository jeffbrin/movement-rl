from movement import Mover, Limb
import numpy as np
import random

class MoverToMujocoConverter:

    @staticmethod
    def _array_to_mujoco_vector(arr: np.ndarray) -> str:
        return f"{arr[0]} {arr[1]} {arr[2]}"

    @staticmethod
    def convert(mover: Mover):
        # limbs don't exist in our MuJoCo world, only segments represent real objects. Iterate through each segment, 
        # for each segment, if a child limb exists, add the limb recursively.

        return f"""
            <body name="mover" euler="0 0 0">
                {MoverToMujocoConverter._convert_limb(mover.torso, np.array([0, 2, 1]))}
            </body>
        """
    
    @staticmethod
    def _convert_limb(limb: Limb, origin_position: np.ndarray[(1, 3), int]) -> str:

        # TODO: ADD SUPPORT FOR MULTIPLE SEGMENTS (CHAINS)
        
        strings = []
        for segment in limb.segments:

            # TODO: THIS WILL NEED TO CHANGE ONCE SEGMENT ORIENTATIONS CAN BE CHANGED
            terminus_position = origin_position - np.array([0, 0, segment.get_length()])

            segment_size = np.array([1, 1, segment.get_length()])
            segment_center_position = (origin_position + terminus_position) / 2

            # Add a body so all child limbs move together when this one moves / rotates
            strings.append(f"""<body 
                           name="{segment.get_name()}-body" 
                           pos="{MoverToMujocoConverter._array_to_mujoco_vector(segment_center_position)}">""")
            
            # Add the segment
            strings.append(f"""<geom 
                           name="{segment.get_name()}-geom" 
                           type="box" 
                           size="{MoverToMujocoConverter._array_to_mujoco_vector(segment_size)}" 
                           pos="{MoverToMujocoConverter._array_to_mujoco_vector(segment_center_position)}"
                           rgba="{random.random()} {random.random()} {random.random()} 1"/>""")
            
            # Add child limbs from origin
            for child_limb in segment.get_origin_child_limbs():
                strings.append(MoverToMujocoConverter._convert_limb(child_limb, origin_position))

            # Add child limbs from terminus
            for child_limb in segment.get_terminus_child_limbs():
                strings.append(MoverToMujocoConverter._convert_limb(child_limb, terminus_position))
            
            # End the body so a sibling segment can move freely
            strings.append(r"""</body>""")

        return "\n".join(strings)
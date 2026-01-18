from enum import Enum
from typing import Optional
from uuid import uuid1

class Limb:

    """
    A limb represents a chain of segments sequentially connected with one or two rotational degrees of freedom.
    For example, a limb could represent a human arm, in which case it would contain three bone segments (upper arm, forearm, hand).
    Segments can also have child limbs. For example, a hand segment would have 5 child limbs, one for each finger.
    A limb does not have to be an appendage. The torso and head for example, could be represented by a limb with child limbs for each appendage.
    
    Generally, segments will represent an extension of a limb, while additional limbs will represent forks or "splits".
    
    """

    def __init__(self, length: float, name: Optional[str] = None):
        """Initializes a limb with one segment of the given length.

        Parameters
        ----------
        length : float
            The length of the first segment in this limb.
        """
        if name is None:
            name = str(uuid1())
        self._name = name
        self.segments: list[Segment] = []

        self.add_segment(Segment(length, self.generate_next_segment_name()))

    def generate_next_segment_name(self) -> str:
        return f"{self._name}-{len(self.segments)}"

    def add_segment(self, segment: "Segment"):
        self.segments.append(segment)


class Segment:
    """
    A segment represents a portion of a limb. For instance, an arm should be modelled as 3 segments (upper arm, lower arm, hand).
    Each segment can also have child limbs. This should be used to create "forking" behaviour where a segment splits into multiple
    "sub-segments." For example, a hand would likely have 5 child limbs: one for each finger.
    """

    class SEGMENT_END(Enum):
        ORIGIN = 0
        TERMINUS = 1

    # TODO: ADD DEGREES OF FREEDOM
    def __init__(self, length: float, name: Optional[str] = None):
        """
        Initializes this segment with the given length. Initializes empty lists for child limbs.

        Parameters
        ----------
        length : float
            The length of this segment. No unit is defined yet.
        """

        self._length: float = length
        self._origin_child_limbs: list[Limb] = []
        self._terminus_child_limbs: list[Limb] = []

        if name is None:
            name = str(uuid1())
        self._name: str = name

    def _add_child_limb(self, limb: Limb, end: SEGMENT_END) -> None:
        """
        Adds a limb to one end of this segment.

        Parameters
        ----------
        limb : Limb
            The child limb to add to this segment.
        end : SEGMENT_END
            The end of the segment to add the limb to. ORIGIN for the start of the limb, TERMINUS for the end.
        """

        if end == Segment.SEGMENT_END.ORIGIN:
            self._origin_child_limbs.append(limb)
        elif end == Segment.SEGMENT_END.TERMINUS:
            self._terminus_child_limbs.append(limb)

    def _get_child_limbs(self, end: SEGMENT_END) -> list[Limb]:
        if end == Segment.SEGMENT_END.ORIGIN:
            return self._origin_child_limbs
        elif end == Segment.SEGMENT_END.TERMINUS:
            return self._terminus_child_limbs

    def _add_child_limbs(self, limbs: list[Limb], end: SEGMENT_END) -> None:
        """
        Adds multiple limbs to one end of this segment.

        Parameters
        ----------
        limbs : list[Limb]
            The list of child limbs to add to this segment.
        end : SEGMENT_END
            The end of the segment to add the limb to. ORIGIN for the start of the limb, TERMINUS for the end.
        """

        for limb in limbs:
            self._add_child_limb(limb, end)

    def add_child_limb_to_origin(self, limb: Limb) -> None:
        """
        Adds a limb to the origin end of this segment.

        Parameters
        ----------
        limb : Limb
            The child limb to add.
        """

        self._add_child_limb(limb, Segment.SEGMENT_END.ORIGIN)

    def add_child_limb_to_terminus(self, limb: Limb) -> None:
        """
        Adds a limb to the terminus end of this segment.

        Parameters
        ----------
        limb : Limb
            The child limb to add to this segment.
        """

        self._add_child_limb(limb, Segment.SEGMENT_END.TERMINUS)

    def get_length(self) -> float:
        return self._length
    
    def get_name(self) -> str:
        return self._name
    
    def get_origin_child_limbs(self) -> list[Limb]:
        return self._get_child_limbs(Segment.SEGMENT_END.ORIGIN)

    def get_terminus_child_limbs(self) -> list[Limb]:
        return self._get_child_limbs(Segment.SEGMENT_END.TERMINUS)
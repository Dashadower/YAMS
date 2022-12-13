from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .pipeline import PipelineCoordinator


class PipelineComponent:
    def on_rising_edge(self, pipeline_c: "PipelineCoordinator") -> None:
        """
        Called for each component, *in order* whenever we're on a rising edge

        :param pipeline_c: PipelineCoordinator for read-only access
        """
        raise NotImplementedError()

    def update(self, pipeline_c: "PipelineCoordinator") -> None:
        """
        This function can be called anytime, which updates a component's internal state, without modifying
        any external components.
        """
        raise NotImplementedError()

    def get_info(self) -> str:
        raise NotImplementedError()
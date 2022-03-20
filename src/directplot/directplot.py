import matplotlib.pyplot as _plt
import inspect as _inspect
from typing import Sequence as _Sequence


class __DirectPlot:
    """Internal class used for the internal singleton object __dp"""

    def __init__(self, titles: _Sequence[str], linesPerSubplot: int = 4, showMarker: bool = True) -> None:
        self._create(titles, linesPerSubplot, showMarker)

    # Besser keinen Destructor. Der löst bei Programm-Ende durch Exceptions weitere Exceptions aus...
    # def __del__(self) -> None:
    #     self.close()

    def _create(self, titles: _Sequence[str], linesPerSubplot: int = 4, showMarker: bool = True) -> None:
        if isinstance(titles, str):
            titles = (titles, )
        
        self.titles = titles
        self.linesPerSubplot = linesPerSubplot

        self.subPlotCount = len(titles)
        if self.subPlotCount<1 or self.subPlotCount>3:
            raise ValueError(f"ERROR in directplot: YOU PROVIDED {self.subPlotCount} PLOT-TITLES. ONLY 1...3 ARE ALLOWED!")

        if not (_plt.isinteractive()): 
            _plt.ion()

        self.xLists=[[]]
        self.yLists=[[]]
        self.lines2d=[]

        self.fig, self.axs = _plt.subplots(1, self.subPlotCount, figsize=(4*self.subPlotCount, 3.5))
        # self.axs soll auch bei nur einem Plot ein Interable sein:
        if self.subPlotCount==1: self.axs = (self.axs, )

        for i, title in enumerate(titles):
            self.axs[i].set_title(title)
            self.axs[i].set_xlabel("xlabel")
            self.axs[i].set_ylabel("ylabel")

            for plot_idx in range(linesPerSubplot):
                newXlist = []
                self.xLists.append(newXlist)
                newYlist = []
                self.yLists.append(newYlist)
                line2d, = self.axs[i].plot(newXlist, newYlist, label=f"id {i*linesPerSubplot+plot_idx}", marker="." if showMarker else "") # marker='o',
                self.lines2d.append(line2d)

            self.axs[i].legend(loc='upper right')
        
        _plt.tight_layout()
        _plt.pause(0.001)
        # self.fig.canvas.draw_idle()
        # self.fig.canvas.start_event_loop(0.001)

    def close(self) -> None:
        try:
            _plt.close(self.fig)
            del(self.xLists)
            del(self.yLists)
            del(self.lines2d)
            del(self.fig)
            del(self.axs)
        except AttributeError:
            raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO PLOT-WINDOW AVAILABLE. DID YOU ALREADY CLOSE IT?")

    def waitforclose(self, msg: str = None) -> None:
        self.fig.canvas.set_window_title(msg or " "+5*" ===== DONE - PLEASE CLOSE THIS WINDOW "+"=====")
        _plt.pause(0.001)
        _plt.ioff()
        _plt.show()
        del(self.xLists)
        del(self.yLists)
        del(self.lines2d)
        del(self.fig)
        del(self.axs)

    def clear(self) -> None:
        self.close()
        self._create(self.titles, self.linesPerSubplot)

    def add(self, id: int, x: float, y: float, refresh: bool = True) -> None:
        if id<0 or id>=self.subPlotCount*self.linesPerSubplot:
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")

        self.xLists[id].append(x)
        self.yLists[id].append(y)
        self.lines2d[id].set_data(self.xLists[id], self.yLists[id])
        if refresh:
            ax_idx = id // self.linesPerSubplot
            self.axs[ax_idx].relim()
            self.axs[ax_idx].autoscale_view()
            _plt.pause(0.001)
            # self.fig.canvas.draw_idle()
            # self.fig.canvas.start_event_loop(0.001)

    def refresh(self) -> None:
        try:
            for ax in self.axs:
                ax.relim()
                ax.autoscale_view()
            _plt.pause(0.001)
            # self.fig.canvas.draw_idle()
            # self.fig.canvas.start_event_loop(0.001)
        except AttributeError:
            raise Exception(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): NO PLOT-WINDOW AVAILABLE. DID YOU ALREADY CLOSE IT?")
    
    def showMarker(self, show: bool = True, id: int = None) -> None:
        if id is None:
            # Alle Linien/Datenserien aktualisieren:
            for line in self.lines2d:
                line.set_marker("." if show else "")
            # Alle Legenden aktualisieren:
            for ax in self.axs:
                ax.legend(loc='upper right')
        else:
            # Nur eine Linie/Datenserie mit Legende aktualisieren:
            if id<0 or id>=len(self.lines2d):
                raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
            self.lines2d[id].set_marker("." if show else "")
            ax_idx = id // self.linesPerSubplot
            self.axs[ax_idx].legend(loc='upper right')
        # Der Einfachheit halber den ganzen Plot aktualisieren:
        _plt.pause(0.001)

    def label(self, id: int, label: str) -> None:
        if id<0 or id>=len(self.lines2d):
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
        self.lines2d[id].set_label(label)
        ax_idx = id // self.linesPerSubplot
        self.axs[ax_idx].legend(loc='upper right')
        _plt.pause(0.001)

    def title(self, id: int, title: str) -> None:
        if id<0 or id>=len(self.lines2d):
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
        ax_idx = id // self.linesPerSubplot
        self.axs[ax_idx].set_title(title)
        self.titles[ax_idx] = title
        _plt.pause(0.001)

    def xylabel(self, id: int, xlabel: str, ylabel: str) -> None:
        if id<0 or id>=len(self.lines2d):
            raise ValueError(f"ERROR in directplot.{_inspect.currentframe().f_code.co_name}(): YOUR id VALUE {id} IS OUT OF THE ALLOWED RANGE OF [0...{len(self.lines2d)-1}]!")
        ax_idx = id // self.linesPerSubplot
        self.axs[ax_idx].set_xlabel(xlabel)
        self.axs[ax_idx].set_ylabel(ylabel)
        _plt.pause(0.001)


#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-


def plot_renko(self, num_bricks=None, signal_indices=None):

    fig, ax = plt.subplots(1, figsize=(10, 5))

    if 'num_bricks' in kwargs:
        pass

    if 'signal_indices' in kwargs:


    # fig.suptitle("Renko Chart (brick size = {})".format(round(self.brick_size, 2)), fontsize=20)
    # ax.set_ylabel('Price ($)')
    # plt.rc('axes', labelsize=20)
    # plt.rc('font', size=16)

    prices = self.renko['price']
    directions = self.renko['direction']

    if num_bricks is not None:
        prices = prices[-num_bricks:]
        directions = directions[-num_bricks:]

    if signal_indices is not None:
        for x in signal_indices:
            plt.axvline(x=x)

    # Calculate range for axis
    ax.set_xlim(0, len(prices) + 1)
    # ax.set_xlim(0, len(self.renko['price']) + 1)
    ax.set_ylim(min(prices) - 2*self.brick_size, max(prices) + 2*self.brick_size)
    # ax.set_ylim(min(self.renko['price']) - 2*self.brick_size, max(self.renko['price']) + 2*self.brick_size)

    # Add bricks to chart
    for x, (price, direction) in enumerate(zip(prices, directions)):
        if direction == 1:
            facecolor='g'
            y = price - self.brick_size
        else:
            facecolor='r'
            y = price

        ax.add_patch(
            Rectangle(
                (x+1, y),
                height=self.brick_size,
                width=1,
                facecolor=facecolor
            )
        )

    return plt.show()

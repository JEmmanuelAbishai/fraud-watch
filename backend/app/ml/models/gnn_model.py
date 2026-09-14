import torch
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv

class FraudGraphSage(torch.nn.Module):
    def __init__(self, in_channels: int, hidden_channels: int = 64, out_channels: int = 2):
        super(FraudGraphSage, self).__init__()
        self.conv1 = SAGEConv(in_channels, hidden_channels)
        self.conv2 = SAGEConv(hidden_channels, out_channels)
        self.lin = torch.nn.Linear(hidden_channels, out_channels)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, p = 0.3, training = self.training)
        x = self.conv2(x, edge_index)
        x = F.relu(x)
        x = self.lin(x)
        return x 
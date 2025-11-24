"""Tower of Hanoi state visualizer"""

class HanoiState:
    def __init__(self, n_disks):
        """Initialize with n disks all on rod A"""
        self.rods = {
            'A': list(range(n_disks, 0, -1)),  # Largest to smallest, top to bottom
            'B': [],
            'C': []
        }
        self.n_disks = n_disks
    
    def move(self, source, target):
        """Move top disk from source to target"""
        if self.rods[source]:
            disk = self.rods[source].pop()
            self.rods[target].append(disk)
    
    def render_html(self):
        """Render the current state as HTML"""
        max_width = 120
        disk_height = 20
        base_height = 8
        rod_width = 4
        rod_height = self.n_disks * disk_height + 20
        
        html = '<div style="display: flex; justify-content: space-around; align-items: flex-end; padding: 15px; background: linear-gradient(to bottom, #e3f2fd 0%, #fff 100%); border-radius: 8px; max-width: 100%; margin: 10px 0;">'
        
        for rod_name in ['A', 'B', 'C']:
            disks = self.rods[rod_name]
            
            # Rod container
            html += '<div style="display: flex; flex-direction: column; align-items: center; flex: 1; margin: 0 5px;">'
            
            # Rod label at top
            html += f'<div style="font-weight: bold; font-size: 14px; margin-bottom: 5px; color: #1976d2;">Rod {rod_name}</div>'
            
            # Tower container with rod and disks
            html += f'<div style="position: relative; width: {max_width + 20}px; height: {rod_height}px; display: flex; flex-direction: column-reverse; align-items: center;">'
            
            # Rod pole (vertical bar in center)
            html += f'<div style="position: absolute; bottom: {base_height}px; left: 50%; transform: translateX(-50%); width: {rod_width}px; height: {rod_height - base_height}px; background: linear-gradient(to bottom, #8d6e63 0%, #5d4037 100%); border-radius: 2px; box-shadow: 1px 1px 3px rgba(0,0,0,0.2); z-index: 0;"></div>'
            
            # Disks (from bottom to top in the list, so we iterate normally)
            disk_bottom = base_height
            for i, disk_size in enumerate(disks):
                disk_width = (max_width * 0.9) * (disk_size / self.n_disks) + (max_width * 0.1)
                # Color gradient based on disk size
                hue = 200 + (disk_size / self.n_disks) * 60  # Blue to cyan spectrum
                
                html += f'''<div style="
                    position: absolute;
                    bottom: {disk_bottom}px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: {disk_width}px;
                    height: {disk_height - 2}px;
                    background: linear-gradient(135deg, hsl({hue}, 70%, 50%) 0%, hsl({hue}, 70%, 60%) 100%);
                    border: 2px solid hsl({hue}, 70%, 30%);
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 12px;
                    color: white;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                    z-index: {i + 1};
                ">{disk_size}</div>'''
                
                disk_bottom += disk_height
            
            html += '</div>'  # Close tower container
            
            # Base
            html += f'<div style="width: {max_width + 20}px; height: {base_height}px; background: linear-gradient(to bottom, #6d4c41 0%, #4e342e 100%); border-radius: 4px; margin-top: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>'
            
            html += '</div>'  # Close rod container
        
        html += '</div>'  # Close main container
        return html


def get_hanoi_state_at_step(n_disks, events, calls, current_step):
    """
    Reconstruct Tower of Hanoi state at a given step by analyzing the recursion trace.
    
    The key insight: 
    - When n=1, the base case executes a move immediately
    - When n>1, the move of disk n happens BETWEEN the two recursive calls:
      1. After tower_of_hanoi(n-1, source, auxiliary, target) completes
      2. Before tower_of_hanoi(n-1, auxiliary, target, source) starts
      
    We track which calls have "completed their first recursive call" to know when to move large disks.
    """
    state = HanoiState(n_disks)
    
    # Track which larger calls (n>1) have completed their first sub-call
    first_subcall_completed = set()
    
    for i in range(current_step):
        event = events[i]
        call = calls[event['call_id']]
        
        if event['type'] == 'end':
            n = call['args'][0]
            source = call['args'][1]
            target = call['args'][2]
            
            if n == 1:
                # Base case: move disk 1 from source to target
                state.move(source, target)
            else:
                # For n>1 calls, when they END, the move has already happened
                #(we handle this when the first subcall completes - see below)
                pass
            
            # Check if this was the first subcall of a parent
            if call['parent_id'] is not None:
                parent = calls[call['parent_id']]
                parent_n = parent['args'][0]
                
                if parent_n > 1 and parent['id'] not in first_subcall_completed:
                    # This call just completed and it was the first subcall of its parent
                    # Now we need to move the parent's disk
                    first_subcall_completed.add(parent['id'])
                    
                    parent_source = parent['args'][1]
                    parent_target = parent['args'][2]
                    
                    # Move disk of size parent_n from parent_source to parent_target
                    state.move(parent_source, parent_target)
    
    return state

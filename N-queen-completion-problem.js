function queens(position, size){
    const to = x => [x[1] == '0'?0:size - +x[1], x[0].charCodeAt() - 97]
    const po = x => String.fromCharCode(97+x[1]) + ((size - x[0]) % 10);
    const S = JSON.stringify;
    position = to(position);
    const is_possible = (p, v) => !([...v].map(JSON.parse).some(x=>x[0]==p[0]||x[1]==p[1]||p[0]+p[1]==x[1]+x[0]||x[1]-x[0]==p[1]-p[0]))
    let visited = new Set([S(position)])
    function DFS(row, visited){
        if(visited.size == size){
            return [...visited].sort().map(x=>po(JSON.parse(x)));
        }
        
        if(row == position[0]) return DFS(row + 1, visited);
        for(let i = 0; i < size; i++){
            if(is_possible([row, i], visited)){
                let V = DFS(row + 1, new Set([...visited, S([row, i])]));
                if(V)
                    return V;
            }
        }
        return false;
    }
    return(DFS(0,visited)+'')
}

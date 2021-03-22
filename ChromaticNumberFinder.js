function helper(adj, colors){
    K = [...Object.keys(adj)]
    function recurse(ind, assignments){
        console.log(ind, K.length)
        if(ind == K.length)
            return true
        let O = {};
        for(let c of colors[K[ind]])
        {
            if(![...adj[K[ind]]].filter(x=>assignments[x]!=undefined).map(x=>assignments[x]).includes(c)){
                O[K[ind]] = c;
                let A = recurse(ind + 1,  {...assignments, ...O});
                if(A)
                    return A;
            }
        }
    }
    return recurse(0, {})
}


function color(M) {
    M = M.trim().split('\n');
    console.log(M)
    let seen = new Set(), stack, current;
    let y, x;
    const H = M.length, W = M[0].length;
    const S = JSON.stringify;
    let neighbours = {};
    for(let i = 0; i < H; i++){
        for(let j = 0; j < W; j++){
            current = [i, j];
            if(!seen.has(S(current))){
                stack = [current];
                while(stack.length){
                    [y, x] = stack.pop();
                    for(let [y_, x_] of [[y, x -1], [y, x + 1], [y - 1, x], [y + 1, x]]){
                        if(y_ > -1 && x_ > -1 && x_ < W && y_ < H && !seen.has(S([y_, x_]))){
                            if(M[y_][x_] == M[i][j])
                                stack.push([y_, x_]);
                            else{
                                neighbours[M[i][j]] = [...(neighbours[M[i][j]]||[]), M[y_][x_]];
                                neighbours[M[y_][x_]] = [...(neighbours[M[y_][x_]]||[]), M[i][j]];
                            }
                        }
                    }
                    seen.add(S([y, x]));
                }
            }
        }
    }

    for(let i in neighbours)
        neighbours[i] = new Set(neighbours[i])

    let X = 'RGB', colors = {};
    for(let i = 1; i <= 3; i++){
        for(let j in neighbours){
            colors[j] = new Set([...X.slice(0, i)]);
        }
        if(helper(neighbours, colors)){
            return i;
        }
    }
    return 4;
}

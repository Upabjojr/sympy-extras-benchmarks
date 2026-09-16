%------------------------------------------------------------------------------
% File     : ARI628_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : Example 0
% Version  : Especial.
% English  :

% Refs     : [ALR14] Avigad et al. (2014), A Heuristic Prover for Real Ineq
%          : [LAR14] Lewis et al. (2014), A Heuristic Prover for Real Inequ
%          : [Lew14] Lewis (2014), Email to Geoff Sutcliffe
% Source   : [Lew14]
% Names    : Example 0 [Lew14]

% Status   : Theorem
% Rating   : 0.50 v9.1.0, 0.60 v9.0.0, 0.50 v8.2.0, 0.33 v7.5.0, 0.40 v7.4.0, 0.50 v7.3.0, 0.38 v7.1.0, 0.50 v7.0.0, 0.67 v6.4.0, 1.00 v6.3.0
% Syntax   : Number of formulae    :   10 (   6 unt;   4 typ;   0 def)
%            Number of atoms       :    6 (   0 equ)
%            Maximal formula atoms :    1 (   1 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    1 (   1 avg)
%            Maximal term depth    :    4 (   1 avg)
%            Number arithmetic     :   15 (   6 atm;   5 fun;   4 num;   0 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    4 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    8 (   4 usr;   7 con; 0-2 aty)
%            Number of variables   :    0 (   0   !;   0   ?;   0   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(y_type,type,
    y: $real ).

tff(x_type,type,
    x: $real ).

tff(v_type,type,
    v: $real ).

tff(u_type,type,
    u: $real ).

tff(hypothesis_00,hypothesis,
    $greater(u,0.0) ).

tff(hypothesis_01,hypothesis,
    $less(u,v) ).

tff(hypothesis_02,hypothesis,
    $less(v,1.0) ).

tff(hypothesis_03,hypothesis,
    $greatereq(x,2.0) ).

tff(hypothesis_04,hypothesis,
    $lesseq(x,y) ).

tff(conclusion,conjecture,
    $less($product($product(2.0,$product(u,u)),x),$product($product(y,y),v)) ).

%------------------------------------------------------------------------------
